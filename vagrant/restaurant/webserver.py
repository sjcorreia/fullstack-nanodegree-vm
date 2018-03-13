from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import cgi

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/edit"):
                addr_path = self.path.split('/')[2]
                print addr_path
                restaurant = session.query(Restaurant).get(addr_path)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Edit the name of restaurant</h1>"
                    output += "<h2>%s</h2>" % restaurant.name
                    output += '''<form method='POST' enctype='multipart/form-data' 
                    action='/restaurants/%d/edit'>
                    <h2>Enter the new name of the restaurant:</h2>''' % restaurant.id
                    output += '''<input name = 'newRestaurantName' 
                    type='text' placeholder = '%s' >''' % restaurant.name
                    output += "<input type = 'submit' value = 'Rename'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
            if self.path.endswith("/delete"):
                addr_path = self.path.split('/')[2]
                print addr_path
                restaurant = session.query(Restaurant).get(addr_path)
                if restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<h1>Delete this restaurant</h1>"
                    output += "<h2>%s</h2>" % restaurant.name
                    output += "<form method='POST' enctype = 'multipart/form-data' action = '/restaurants/%s/delete'>" % addr_path
                    output += "<input type = 'submit' value = 'Delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Create a new restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                action='/restaurants/new'>
                <h2>Enter the name of the new restaurant:</h2><input 
                name="message" type="text" >
                <input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants</h1>"
                output += "<a href='/restaurants/new'>Create a new restaurant here</a>"
                output += "</br></br>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br><a href='/restaurants/%d/edit'>Edit</a>" % restaurant.id
                    output += "</br><a href='/restaurants/%d/delete'>Delete</a>" % restaurant.id
                    output += "</br></br></br>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                action='/hello'><h2>What would you like me to say?</h2><input 
                name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>&#161Hola!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' 
                action='/hello'><h2>What would you like me to say?</h2><input 
                name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                addr_path = self.path.split('/')[2]

                # Delete this restaurant from the database
                deleteRestaurant = session.query(Restaurant).filter_by(id=addr_path).one()
                if deleteRestaurant:
                    session.delete(deleteRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                else:
                    print "didn't work"
                return
            if self.path.endswith("/edit"):
                # restaurant = session.query(Restaurant).get(addr_path[1])
                print "Edit the restaurant name"

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':  
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    addr_path = self.path.split('/')[2]

                print "before assigning the new name"
                print addr_path
                # Update the name of the restaurant
                editRestaurant = session.query(Restaurant).filter_by(id = addr_path).one()
                if editRestaurant != []:
                    editRestaurant.name = messagecontent[0]
                    session.add(editRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                else:
                    print "didn't work"
                return

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':  
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                
                # Create new restaurant
                newRestaurant = Restaurant(name=messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            else:
                self.send_response(301)
                self.end_headers()

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')
                output = ""
                output += "<html><body>"
                output += " <h2> Let's add a new restaurant </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]
                output += '''<form method='POST' enctype='multipart/form-data' 
                action='/restaurants'><h2>new restaurant?</h2><input 
                name="message" type="text" >
                <input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except:
            self.send_error(404, 'File Not Found: %s' % self.path)


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()


if __name__ == '__main__':
    main()
