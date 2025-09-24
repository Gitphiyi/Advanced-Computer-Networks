#pragma once
#define PORT 8080

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <iostream>

int init_socket(const char* host, int port);
void parse_packet();