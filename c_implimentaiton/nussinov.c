#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <argp.h>
#include <regex.h>

#define DEGUG()

int COMMON = 1;

const char *argp_program_version = "nussinov .1";
const char *argp_program_bug_address = "<jmwolff3@illinois.edu>";

/* Program Documentation */
static char doc[] = "Nussinov Solver -- a solver for optimal substructure for RNA sequences.";

static char args_doc[] = "verbose";
/* Argument Parser

 */
static struct argp_option options[] = {
    {"verbose", 'v',    0,  0,  "Produce Verbose Output"},
    {"quiet",   'q',    0,  0,  "Produce No Output"},
    {"sequence",    's',    "SEQUENCE",  0,  "RNA Sequence String"},
    {"uncommon",    'u',    0,  0,  "Use Uncommon Matches"},
    // {"file",    'f',    "FILEPATH",  0,  "Path to file containing RNA Sequence"},
    { 0 }
};

struct arguments {
    int verbose, quiet;
    char * sequence;
    char * filepath;
};

struct node {
    int a, b;
    struct node * next;
    struct node * prev;
};

struct node * head;
struct node * tail;

void add_node(int a, int b) {
    struct node * n = malloc(sizeof(struct node));
    n->a = a;
    n->b = b;
    n->next = NULL;
    n->prev = NULL;

    if(head) {
        tail->next = n;
        n->prev = tail;
        tail = n;
    }
    else {
        head = n;
        tail = n;
    }
}

void free_nodes() {
    while(head) {
        struct node * tmp = head->next;
        free(head);
        head = tmp;
    }
}

static error_t parse_opt(int key, char *arg, struct argp_state *state) {
    struct arguments * arguments = state->input;

    switch(key) {
        case 'v':
            arguments->verbose = 1;
            break;
        case 'q':
            arguments->quiet = 1;
            break;
        case 's':
            arguments->sequence = arg;
            break;
        case 'u':
            COMMON = 0;
            break;
        // case 'f':
            // arguments->filepath = arg;
            // break;
        case ARGP_KEY_ARG:
            return 0;
        default:
            return ARGP_ERR_UNKNOWN;
    }
    return 0;
}

void get_sequence(struct arguments * arguments) {
    printf("%s\n", arguments->filepath);
    // check if the path exists

    // load the file

    // save the string as sequence
}

int check_validity(struct arguments * arguments) {
    for(int i = 0; i < strlen(arguments->sequence); i++) {
        arguments->sequence[i] = toupper(arguments->sequence[i]);
        char cur = arguments->sequence[i];
        if(cur != 'A' && cur != 'C' && cur != 'G' && cur != 'U')
            return 0;
    }
    return 1;
}

int cost_function(char a, char b) {
    if ((a == 'A' && b == 'U') || (a =='U' && b =='A'))
        return 1;
    if ((a == 'G' && b == 'C') || (a =='C' && b == 'G'))
        return 1;
    if (!COMMON) {
        if ((a == 'G' && b == 'U') || (a == 'U' && b == 'G'))
            return 1;
    }
    return 0;
}

static struct argp argp = {options, parse_opt, args_doc, doc, 0, 0, 0};

void classical_nussinov(struct arguments * arguments, int ** matrix, int length) {
    char * sequence = arguments->sequence;
    for (int d = 1; d < length; d++) {
        for (int i = 0; i < length-d; i++) {
            int j = i+d;
            int temp = matrix[i+1][j-1] + cost_function(sequence[i], sequence[j]);
            for (int k =i; k < j; k++) {
                int other = matrix[i][k]+matrix[k+1][j];
                if (other > temp) {
                    temp = other;
                }
            }
            matrix[i][j] = temp;
        }
    }
    return;
}

void backtrace(char * sequence, int ** matrix, int i, int j) {
    if (j <= i)
        return;

    if (matrix[i][j] == matrix[i][j-1])
        backtrace(sequence, matrix, i, j-1);
    else {
        for(int k = i; k < j; k++) {
            if (cost_function(sequence[k], sequence[j])) {
                if (k-1 < 0) {
                    if (matrix[i][j] == matrix[k+1][j-1]+1) {
                        add_node(k,j);
                        backtrace(sequence, matrix, k+1, j-1);
                    }
                }
                if (matrix[i][j] == matrix[i][k-1] + matrix[k+1][j-1] + 1) {
                    add_node(k, j);
                    backtrace(sequence, matrix, i, k-1);
                    backtrace(sequence, matrix, k+1, j-1);
                    break;
                }
            }
        }
    }
}

int ** allocate_matrix(int length) {
    int ** m = malloc(length*sizeof(int*));
    for (int i = 0; i < length; i++) {
        m[i] = calloc(length, sizeof(int));
    }
    return m;
}

void free_matrix(int **m, int length) {
    for(int i = 0; i < length; i++) {
        free(m[i]);
    }
    free(m);
}

void print_matrix(int ** m, int length) {
    for (int i = 0; i < length; i++) {
        for (int j = 0; j < length; j++) {
            printf("%d  ", m[i][j]);
        }
        printf("\n");
    }
}

void print_substructure(char * sequence) {
    printf("%s\n", sequence);
    char * structure = malloc(strlen(sequence)+1);
    memset(structure, 0x2E, strlen(sequence));
    struct node * cur = head;
    while(cur) {
        structure[cur->a] = '(';
        structure[cur->b] = ')';
        cur = cur->next;
    }
    printf("%s\n", structure);
    free(structure);
}

int main(int argc, char *argv[]) {
    struct arguments arguments;
    arguments.filepath = NULL;
    arguments.sequence = NULL;
    argp_parse(&argp, argc, argv, 0, 0, &arguments);
    if(arguments.filepath) {
        get_sequence(&arguments);
    }

    printf("%s\n", arguments.sequence);

    if (!check_validity(&arguments)) {
        printf("Invalid characters in sequence.\n");
        exit(1);
    }

    int length = strlen(arguments.sequence);
    int ** matrix = allocate_matrix(length);
    if (matrix == NULL) {
        perror("Malloc failed");
        exit(1);
    }
    classical_nussinov(&arguments, matrix, length);
    backtrace(arguments.sequence, matrix, 0, length-1);
    print_matrix(matrix, length);

    print_substructure(arguments.sequence);

    free_matrix(matrix, length);
    free_nodes();
    return 0;
}