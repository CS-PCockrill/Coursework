/*
* Patrick Cockrill, G01127120
* Professor Mengistu
* CS 262-004, Lab 212
* Project 2
*/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<ctype.h>

typedef struct pair {
  int count;
  int **indices;
} pair;

void print_menu(int *option) {
  int input;
  /* This is pretty self explanatory. Menu that prints options to console for user to select 1-4 */
  printf("1) Read in the name of a text file to use as a cipher key\n");
  printf("2) Create a cipher using the input text file (and save the result to a file)\n");
  printf("3) Decode an existing cipher (prompt user for a file to read containing cipher)\n");
  printf("4) Exit the program.\n");
  printf("Enter your choice:\n");
  scanf("%d", &input);
  getchar();
  *option = input;
}

int readFile(char **words, char *file) {
  FILE *read;
  char line;
  int wordCount;
  int j;

  /* read IN a file to then iterate through and add each word in the file to a character array */
  printf("Enter the name of text file:\n");
  scanf("%s", file);
  read = fopen(file, "r");

  j = 0;
  wordCount = 0;
  /* if the file is non-null... */
  if (read != NULL) {
    /* get the first character in the file */
    line = fgetc(read);
    while (line != EOF) {
      /* while line doesn't reach EOF... check for spaces and newline characters and
      * increase wordcount, and terminate the previous word with null-character */
      if (line == ' ' || line == '\n') {
        words[wordCount][j++] = '\0';
        wordCount++;
        j = 0;
      } else {
        /* otherwise, put each character of the word in the words array */
        words[wordCount][j++] = tolower(line);
      }
      /* Then get next character */
      line = fgetc(read);
    }
  } else {
    /* If file doesn't exist print ERROR to console and return 0 count */
    printf("ERROR: File does not exist...\n");
    file = NULL;
    return 0;
  }
  /* Close the file and return word count if file was non-null and successful */
  fclose(read);
  printf("%d\n", wordCount);
  return wordCount;
}

void encode(char **words, char *filename, int wordcount) {
  FILE *ciphptr;
  char line[1500];

  int i = 0, letter = 0;
  int word = 0;
  int flag;
  int count;
  int n;
  pair *arr;
  /* int j, z; */

  /* If the file is empty, then call ReadFile() to input a text file */
  if (strcmp(filename, "") == 0) {
    wordcount = readFile(words, filename);
  }

  /* Then, prompt user to enter a message they would like to encrypt, using
  * fgets() to specify max length */
  printf("Enter a message you'd like to encrypt (and press enter): ");
  fgets(line, 1500, stdin);
  ciphptr = fopen("cipher-text.txt", "w");
  arr = (int *) malloc(26 * sizeof(pair));

  /*
  for (j = 0; j < wordcount; j++) {
    for (z = 0; z < strlen(words[j]); z++) {
      int indice = (tolower(words[j][z]) - 'a');
      arr[indice].count += 1;
      // arr[indice].indices = {j, z};
    }
  }
  */

  /* While the secret message is not at its end */
  n = rand() % 10;
  while (line[i] != '\0') {
    /* Start iteration at the 0'th word and go till we run out of words to check */
    word = 0;
    while (word < wordcount) {
      letter = 0;
      flag = 0;
      while (words[word][letter] != '\0') {
        /* As far as I know from instructions, if a space occurs, we add an additional space in between encoded pairs */
        if (line[i] == ' ') {
          printf("%c --> ' '\n", line[i]);
          fprintf(ciphptr, "%c", ' ');
          flag = 1;
          break;
        }
        if (tolower(line[i]) == words[word][letter]) {
            printf("%c --> %d, %d\n", line[i], word, letter);

            if (ciphptr) {
              fprintf(ciphptr, "%d ", word);
              fprintf(ciphptr, "%d ", letter);
            }
            flag = 1;

            /* FIXME: Here we have to loop through the options of the letter options
            using a random number, or store each option as a temp array and
            find the i'th index in the array as our final cipher location */

	           /* As long as the file to write to isn't NULL, write each word/letter
 	           * location into the file, respectively */

            /* Here when a letter is found (in the words array), it is flagged and we 		will break and
 	          * move forward to the next character to be encoded.*/
            break;
        }

        letter++;
      }

      /* When it has been found break out of this loop */
      if (flag == 1) {
        break;
      }

      word++;
    }

    /* NEED TO FIND n'th CHARACTER BEFORE GOING TO I++ (NEXT CHARACTER ENCODING) */
    i++;
  }
  /* Close file */
  fclose(ciphptr);

}

void decode(char **words, char *cipherFile, char *textfile, int wordCount) {
  FILE *ciphptr;
  char message[1500];
  int c;
  char line;
  int i;
  int j;

  int letter;
  int wordpos;
  int letterpos;

  i = 0;
  j = 0;

  if (strcmp(textfile, "") == 0) {
     wordCount = readFile(words, textfile);
     encode(words, textfile, wordCount);
     do {
        c = getchar();
     } while (c != EOF && c != '\n');
  }

  printf("Enter the name of the cipher file (File with number pairs):\n");
  scanf("%s", cipherFile);

  ciphptr = fopen(cipherFile, "r");
  /* check if non-null, if non-null get the characters from cipher-text.txt one at
 * a time and put that character in message character array */
  if (ciphptr != NULL) {
    line = fgetc(ciphptr);
    while (line != EOF) {
      /* ignore spaces and newlines (jump over them) by calling fgetc() again */
      if (line == ' ' && line != '\n') {
        line = fgetc(ciphptr);
      }
      /* add character to message array to later act as indices in loop below this */
      message[i] = line;
      line = fgetc(ciphptr);
      i++;
    }
  } else {
    printf("ERROR: File not found.\n");
    cipherFile = NULL;
    return;
  }
  /* j < i-1 because at i there is a garbage character that should be ignored,
 * and I found i-1 to be best solution to this issue */
  while (j < i-1) {
    letter = j;
    /* if the index is a space, print a space */
    if (message[j] == ' ') {
      printf(" ");
      j++;
      continue;
    }
    /* wordpos/letter pos converts ordered pair values into ints,
 * which will act as the indices in the words of (origin) file */
    wordpos = (int)(message[j]) - 48;
    letterpos = (int)(message[letter+1]) - 48;
    printf("%c", words[wordpos][letterpos]);
    j += 2;
  }
  /* print newline, since we are printing decoded text to console.
 * and close file */
  printf("\n");
  fclose(ciphptr);

}

int main() {
  char **words;
  char *file;
  char *cipherfile;
  int i;
  int option;
  int wordCount;
  srand(7120);
  /* G01127120 */


  wordCount = 0;
  /* wordCount = (int *) malloc(sizeof(int *)); */
  /* FixME: This number shouldn't be static */
  words = (char **) malloc(5000 * sizeof(char *));

  for(i=0; i<5000; i++) {
    words[i] = (char *) malloc(15 * sizeof(char));
  }
  /* 25 * sizeof(char) = 25 * 1 = 25, accomadating for
  * filename of length 25
  */
  file = (char *) malloc(25*sizeof(char));
  cipherfile = (char *) malloc(25 * sizeof(char));

  /* For some reason, the only way it works currently is if you run through option 1, then 2, then 3... I've been tinkering with it to fix it but there is nothing I am seeing that causes the behavior of choosing option 3 first to actually cause the problem its causing */
  while (1) {
    print_menu(&option);
    switch(option) {
      case 1:
        wordCount = readFile(words, file);

        break;
      case 2:
        encode(words, file, wordCount);
        /* Encode text file */
        break;
      case 3:
        /* Decode ciphertext file */
        decode(words, cipherfile, file, wordCount);
        break;
      case 4:
        printf("Quitting program... come again.\n");
        exit(0);
      default:
        printf("Invalid entry... please try again.\n");
    }
  }
  free(words);
  free(file);
  free(cipherfile);

  return 0;
}
