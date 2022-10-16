#include<string.h>
#include<unistd.h>
#include<stdlib.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<fcntl.h>

#define BUFF_SIZE 1024
int text_output(char [], int);

int main(int argc, char *argv[]) {
    int file_id, size;
    char str[BUFF_SIZE];

    char msg_open_error[] = "E: No input file, exit.";
    char msg_copy[] = "Copy_Successful";
    char msg_move[] = "Move_Successful";

    if (argc == 1) {
        file_id = open("logfile.txt", O_RDONLY);

        if (file_id == -1) {
            text_output(msg_open_error, sizeof(msg_open_error));
            exit(EXIT_FAILURE);
        }

        size = read(file_id, str, sizeof(str));
        close(file_id);
        text_output(str, size);
        exit(EXIT_SUCCESS);
    }
   /* 
    else if (argc >= 3) {
        
    }
*/
    else {
        file_id = open(argv[1], O_RDONLY);
        size = read(file_id, str, sizeof(str));
        close(file_id);
        text_output(str, size);
        exit(EXIT_SUCCESS);
    }
    return 0;

}

int text_output(char str[], int size) {
    int lenght;
    write(1, str, size);
    lenght = read(0, str, size);
    return lenght;
}
