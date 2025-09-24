#include "server.hpp"
#include "client.hpp"

#include <iostream>

int main() {
    std::cout << "HTTP demo\n";
    const char* ipv6 = "0::1";
    int port = 8080;
    int server_fd = init_socket(ipv6, port);
    connect_to_server(server_fd, ipv6, port);
    connect_to_client(server_fd);
    return 1;
}