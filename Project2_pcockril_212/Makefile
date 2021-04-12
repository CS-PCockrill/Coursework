# A simple Makefile
# Patrick Cockrill, G01127120
# CS 262, Lab Section 212
# Lab 2
# The compiler: gcc for C programs, g++ for C++ programs, etc

CC = gcc

CFLAGS= -Wall -g -O2 -std=c89 -D_XOPEN_SOURCE=600 -pedantic-errors
LIBS=-lm
TARGET = Project2_pcockril_212

$(TARGET): $(TARGET).c 
	$(CC) $(CFLAGS) -o $(TARGET) $(TARGET).c 
clean: 
	rm $(TARGET)
