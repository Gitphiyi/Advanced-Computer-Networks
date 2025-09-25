#pragma once
#define PORT 8080

#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <iostream>
#include <unordered_set>

enum class RequestMethod {
    GET,  // get data
    HEAD, // same as GET but only get headers
    POST, // submit data
    PUT,
    PATCH, // modify something
    DELETE,
    OPTIONS,
    CONNECT
};
enum class ConnectionType {
    CLOSE,
    KEEPALIVE,
    UPGRADE,
    MULTIPLEXED
};

std::unordered_set<std::string> accepted_types = {};

struct http_request_header {
    RequestMethod       request_type; //GET, POST, etc.
    std::string         resource_path; // path to resource. receiver determines what this path means
    float               version; // 1.1, 1.2, etc
    std::string         host; // i.e. www.host.com It specifies which domain a sender wants
    std::string         user_agent; // browser, OS, engine
    std::string         accept_types;  
    std::string         accept_langs; // English, Chinese, etc.
    std::string         accept_encoding; //gzip, brotli, etc.
    std::string         referer; // previous page that sent the request
    ConnectionType      connection;
    bool                upgrade_insecure_req;
};

struct http_request {
    http_request_header header;
    std::byte*          body; // byte array
};

int init_socket(const char* host, int port);
void parse_packet();
std::string encode_http(http_request_header header);
http_request_header decode_http(std::string header);