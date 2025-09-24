#include "server.hpp"
#include <system_error>
#include <cerrno>

/**
 * returns socket file descriptor
 */
int init_socket(const char* ip, int port) {
    int return_val;
    // Create Socket
    int fd = socket(AF_INET6, SOCK_STREAM, 0); //AF_INET specifies socket is for IPv6 communication. SOCK_STREAM specifies it's a TCP socket. 
    if(fd == -1) {
        std::system_error(errno, std::generic_category(), "failed to create socket");
    }

    // Tell socket it is going to get data from specified IP and port
    struct sockaddr_in6 ip_addr; // IPv6 address
    memset(&ip_addr, 0, sizeof(ip_addr));
    ip_addr.sin6_family = AF_INET6;
    return_val = inet_pton(AF_INET6, ip, &ip_addr.sin6_addr); //sets string IP to binary form
    if(return_val == -1) {
        std::system_error(errno, std::generic_category(), "failed to convert string IP to binary form");
    }
    ip_addr.sin6_port = htons(port); // turns port into network byte oriented port num
    return_val = bind(fd, reinterpret_cast<const sockaddr*>(&ip_addr), sizeof(ip_addr));
    if(return_val == -1) {
        std::system_error(errno, std::generic_category(), "failed to bind to IP and port");
    }
    return fd;
    // Close socket when finished with connection
}

int connect_to_client(int socket_fd) {
    int return_val;

    // start of TCP handshake on server's side
    return_val = listen(socket_fd, BACKLOG); // keeps a queue of SYNs received
    if(return_val == -1) {
        std::system_error(errno, std::generic_category(), "failed to listen at socket");
    }
    
    // finishes TCP Handshake with client and establish connection with client
    struct sockaddr_in6* client_ip; //optional buffer where client_ip is stored
    socklen_t client_ip_sz = sizeof(sockaddr_in6);
    int connection_fd = accept(socket_fd, reinterpret_cast<struct sockaddr*>(client_ip), &client_ip_sz); // new fd made for specific TCP connection
    if(connection_fd == -1) {
        std::system_error(errno, std::generic_category(), "failed to accept connection request");
    }
    std::cout<<"Connected to client!\n";
    return connection_fd;
}