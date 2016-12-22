
import socket
import sys
import threading

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#proses binding
server_address = ('localhost', 13006)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

#listening
sock.listen(1)


def response_teks():
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: text/plain\r\n" \
		"Content-Length: 7\r\n" \
		"\r\n" \
		"PROGJAR"
	return hasil

def response_gambar():
	filegambar = open('gambar.png','r').read()
	panjang = len(filegambar)
	hasil = "HTTP/1.1 200 OK\r\n" \
		"Content-Type: image/png\r\n" \
		"Content-Length: {}\r\n" \
		"\r\n" \
		"{}" . format(panjang, filegambar)
	return hasil

def response_page(url):
    filename = url.split("/")
    filename = filename[1]
    print "filename : "+filename
    
    filename = "pages/"+filename
    
    try:
        webfile = open(filename, 'r').read()
    except:
        webfile = open('pages/not_found.html').read()
    
    length = len(webfile)
    hasil = "HTTP/1.1 200 OK\r\n" \
    		"Content-Type: text/html;charset=UTF-8" \
    		"Content-Length: {}\r\n" \
    		"\r\n" \
    		"{}" . format(length, webfile)
    return hasil

def response_document(url):
    n = len(url)
    filename = url[1:n]
    print "filename : "+filename
    
    docfile = open(filename, 'r').read()
    
    length = len(docfile)
    hasil = "HTTP/1.1 200 OK\r\n" \
    		"Content-Type: application/pdf" \
    		"Content-Length: {}\r\n" \
    		"\r\n" \
    		"{}" . format(length, docfile)
    return hasil

#fungsi melayani client
def layani_client(koneksi_client,alamat_client):
    try:
       print >>sys.stderr, 'ada koneksi dari ', alamat_client
       request_message = ''
       while True:
           data = koneksi_client.recv(64)
           data = bytes.decode(data)
           request_message = request_message+data
           if (request_message[-4:]=="\r\n\r\n"):
               break
    

       baris = request_message.split("\r\n")
       baris_request = baris[0]
       print "baris request[0] : "+baris_request
  
       a,url,c = baris_request.split(" ")
       print "url : "+url
       
       ekstensi = url.split(".")
       ekstensi = ekstensi[1]
       
       respon = ""
       if (ekstensi=='html'):
          respon = response_page(url)
       else:
           respon = response_document(url)
       koneksi_client.send(respon)
    finally:
        # Clean up the connection
        koneksi_client.close()


while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    s = threading.Thread(target=layani_client, args=(koneksi_client,alamat_client))
    s.start()


