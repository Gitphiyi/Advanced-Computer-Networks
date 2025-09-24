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

    char buffer[5];
    char recv_buffer[5];
    const char* msg = "hello";
    memcpy(buffer, msg, 5);
    send(server_fd, buffer, 5, 0);
    ssize_t received_bytes = recv(server_fd, recv_buffer, 5, 0);
    if(received_bytes != -1) {
        std::cout << "server received " << received_bytes << "bytes\n";
        for(int i = 0; i < 5; i++) {
            std::cout<<recv_buffer[i];
        }
    }
    return 1;
}