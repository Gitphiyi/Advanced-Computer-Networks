#pragma once

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <iostream>

#define BACKLOG 128 // how many incoming

int init_socket(const char* ip, int port);
int connect_to_client(int socket_fd);