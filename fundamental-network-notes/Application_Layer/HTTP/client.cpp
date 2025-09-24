#include "client.hpp"

#include <system_error>
#include <cerrno>

int connect_to_server(int server_fd, const char* ip, int port) {
    struct sockaddr_in6 server_ip;
    memset(&server_ip, 0, sizeof(server_ip));
    server_ip.sin6_family = AF_INET6;
    server_ip.sin6_port = htons(port);
    inet_pton(AF_INET6, ip, &server_ip.sin6_addr);

    // Starts TCP Handshake with server
    if(connect(server_fd, reinterpret_cast<const sockaddr*>(&server_ip), sizeof(server_ip)) == -1) {
        std::system_error(errno, std::generic_category(), "failed to connect to server");
        close(server_fd);
        return -1;
    }
    std::cout<<"Connected to server!\n";
    return 0;
}