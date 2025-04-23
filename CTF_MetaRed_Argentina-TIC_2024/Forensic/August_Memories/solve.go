package main

import (
    "bytes"
    "encoding/hex"
    "fmt"
    "log"
    "os"
    "os/exec"
    "strings"
)

// USB HID keyboard mapping
var hidKeyboard = map[byte]string{
    0x04: "a", 0x05: "b", 0x06: "c", 0x07: "d", 0x08: "e",
    0x09: "f", 0x0A: "g", 0x0B: "h", 0x0C: "i", 0x0D: "j",
    0x0E: "k", 0x0F: "l", 0x10: "m", 0x11: "n", 0x12: "o",
    0x13: "p", 0x14: "q", 0x15: "r", 0x16: "s", 0x17: "t",
    0x18: "u", 0x19: "v", 0x1A: "w", 0x1B: "x", 0x1C: "y",
    0x1D: "z", 0x1E: "1", 0x1F: "2", 0x20: "3", 0x21: "4",
    0x22: "5", 0x23: "6", 0x24: "7", 0x25: "8", 0x26: "9",
    0x27: "0", 0x28: "\n", 0x29: "[ESC]", 0x2A: "[BACKSPACE]",
    0x2B: "\t", 0x2C: " ", 0x2D: "-", 0x2E: "=", 0x2F: "[",
    0x30: "]", 0x31: "\\", 0x33: ";", 0x34: "'", 0x35: "`",
    0x36: ",", 0x37: ".", 0x38: "/", 0x39: "[CAPS]",
    0x4F: "→", 0x50: "←", 0x51: "↓", 0x52: "↑",
}

func extractKeyboardData(pcapFile string) (string, error) {
    // tshark command to extract USB keyboard data
    cmd := exec.Command("tshark", "-r", pcapFile, "-Y", "usb.transfer_type == 0x01 && usb.data_len == 8", "-T", "fields", "-e", "usb.capdata")
    output, err := cmd.Output()
    if err != nil {
        return "", fmt.Errorf("error running tshark: %v", err)
    }

    var pressedKeys []string
    lines := bytes.Split(output, []byte{'\n'})
    for _, line := range lines {
        if len(line) == 0 {
            continue
        }

        // Convert hex string to bytes
        data, err := hex.DecodeString(strings.ReplaceAll(string(line), ":", ""))
        if err != nil {
            continue
        }

        // The third byte (data[2]) contains the key code
        if len(data) >= 3 && data[2] != 0x00 {
            keyCode := data[2]
            fmt.Print(keyCode," ")
            if key, exists := hidKeyboard[keyCode]; exists {
                pressedKeys = append(pressedKeys, key)
            }
        }
    }

    return strings.Join(pressedKeys, ""), nil
}

func main() {
    if len(os.Args) != 2 {
        fmt.Printf("Usage: %s <pcap_file>\n", os.Args[0])
        os.Exit(1)
    }

    pcapFile := os.Args[1]
    keyboardInput, err := extractKeyboardData(pcapFile)
    if err != nil {
        log.Fatalf("Failed to extract keyboard data: %v", err)
    }

    if len(keyboardInput) > 0 {
        fmt.Println("\nExtracted keyboard input:")
        fmt.Println(keyboardInput)
    } else {
        fmt.Println("\nNo keyboard input found or error processing file.")
    }
}
