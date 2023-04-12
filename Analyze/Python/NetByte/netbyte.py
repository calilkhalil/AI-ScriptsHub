import struct
import socket
import datetime
import argparse

def analyze_packet(packet):
    # Lendo os primeiros 20 bytes do pacote
    ip_header = packet[0:20]

    # Decodificando o cabeçalho IP
    fields = struct.unpack("!BBHHHBBH4s4s", ip_header)

    version = fields[0] >> 4
    header_length = (fields[0] & 0xF) * 4
    ttl = fields[5]
    protocol_num = fields[6]
    src_ip = socket.inet_ntoa(fields[8])
    dest_ip = socket.inet_ntoa(fields[9])

    # Decodificando o cabeçalho TCP
    tcp_header = packet[header_length:header_length+20]
    fields = struct.unpack("!HHLLBBHHH", tcp_header)

    src_port = fields[0]
    dest_port = fields[1]
    seq_num = fields[2]
    ack_num = fields[3]
    offset = fields[4] >> 4
    flags = fields[5]
    window_size = fields[6]

    # Convertendo a data e hora para formato legível
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Imprimindo as informações relevantes
    print("Packet captured at: {}".format(timestamp))
    print("Protocol: TCP")
    print("Source IP: {}".format(src_ip))
    print("Destination IP: {}".format(dest_ip))
    print("Source Port: {}".format(src_port))
    print("Destination Port: {}".format(dest_port))
    print("Sequence Number: {}".format(seq_num))
    print("Acknowledgement Number: {}".format(ack_num))
    print("Flags: {}".format(flags))
    print("Window Size: {}".format(window_size))


if __name__ == '__main__':
    # Criando um parser para receber o caminho do arquivo como parâmetro
    parser = argparse.ArgumentParser(description='Analyze network packets')
    parser.add_argument('file_path', metavar='file_path', type=str, help='Path to the packet capture file')

    args = parser.parse_args()

    # Lendo o conteúdo do arquivo
    with open(args.file_path, 'rb') as file:
        data = file.read()

    # Analisando os pacotes
    packet_num = 1
    while data:
        packet = data[:54]
        data = data[54:]
        print("Packet {}:".format(packet_num))
        analyze_packet(packet)
        packet_num += 1
