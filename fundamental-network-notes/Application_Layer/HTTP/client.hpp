#pragma once

#include "general.hpp"

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <iostream>

int connect_to_server(int server_fd, const char* ip, int port);
void send_http_bytes(int server_fd, http_request request);