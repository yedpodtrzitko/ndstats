package main

import (
    "os"
    "net"
    "fmt"
    "regexp"
    "strconv"
    "github.com/adjust/redismq"
)

const (
    CONN_PORT = "27500"
    CONN_TYPE = "udp"
    BOT_RE = `^".*?<\d+><BOT><.*?>"`
)

var reBot, _ = regexp.Compile(BOT_RE)

func CheckError(err error) {
    if err != nil {
        fmt.Println("cant bind socket")
        os.Exit(1)
    }
}

func main() {
    ServerAddr, err := net.ResolveUDPAddr(CONN_TYPE, ":" + CONN_PORT)
    CheckError(err)
    fmt.Println("Listening on :" + CONN_PORT)

    // Close the listener when the application closes.
	conn, err := net.ListenUDP(CONN_TYPE, ServerAddr)
	CheckError(err)
	defer conn.Close()

    q := redismq.CreateQueue("localhost", "6379", "", 0, "ndstats")

    for {
        handleLine(q, conn)
    }
}

func handleLine(q *redismq.Queue, conn *net.UDPConn) {
    buf := make([]byte, 1024)

    msgLen, addr, err := conn.ReadFromUDP(buf)
    if err != nil {
        fmt.Println("Error reading:", err.Error())
        return
    }

    msgString := string(buf[4:msgLen])

    botMatch := reBot.MatchString(msgString)
    if (botMatch) {
        return
    }

    finalMsg := addr.IP.String() + ":" +  strconv.Itoa(addr.Port) +"|" + msgString

    fmt.Println("formatted message: ", finalMsg)

    q.Put(finalMsg)
    // redismq::ndstats
}
