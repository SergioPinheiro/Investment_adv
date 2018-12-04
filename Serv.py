from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from Client import Client
from Enterprise import  Enterprise
from Article import Article
from dataset import dataset
from random import normalvariate
from random import choices
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd

class Serv(BaseHTTPRequestHandler):

    # def __init__(self):
    #     self.elementos = []

    knn = KNeighborsClassifier(n_neighbors=1)

    enterprises = [Enterprise("Microsoft", 1, [0]),
               Enterprise("Apple", 1, [0]),
               Enterprise("Google", 1, [0]),
               Enterprise("IBM", 1, [0]),
               Enterprise("Amazon", 1, [0]),
               Enterprise("eBay", 1, [0]),
               Enterprise("Sony", 1, [0]),
               Enterprise("Samsung", 1, [0]),
               Enterprise("HP", 1, [0]),
               Enterprise("Dell", 1, [0])
               ]

    clients = [Client("Sergio", 2),
           Client("Joao", 1),
           Client("Maria", 3),
           Client("Jose", 1),
           Client("Thiago", 3),
           Client("Luana", 2),
           Client("Gabriela", 1)
           ]

    dataset = dataset()

    last_articles = dict()


    def _set_headers(self):
        # self.send_response(200)
        # self.send_header('Content-type', 'text/html')
        # self.end_headers()
        pass

    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        try:
            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".ico"):
                mimetype='image/ico'
                sendReply = True
            if self.path.endswith(".png"):
                mimetype='image/png'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
				#Open the static file requested and send it
                f = open("./web" + self.path, "r", errors='ignore')#, encoding="utf-8")
                self.train()
                self.make_articles(100)
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(bytes(f.read(), 'utf-8'))
                # self.wfile.write(json.dumps(self.enterprises).encode())
                f.close()
                return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # print ("in post method")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        # data = json.loads(self.data_string)
        #print(data)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        # self.wfile.write(bytes("hello"), 'utf-8')
        #try:
        self.wfile.write(json.dumps(self.adv()).encode())
        #except:
         #   print('Dijkstra error!')
        return

    def adv(self):
        ret = dict()
        ret['news'] = self.last_articles
        ret['clients'] = self.users()
        ret['enterprises'] = self.companys()
        ret['adv'] = self.predict(1, 5)
        return ret

    def new_article(self):
        ent = choices(self.enterprises)
        news = round(normalvariate(0,1), 4)
        ent[0].rate += news
        ent[0].risk.append(news)
        self.last_articles[ent[0].name] = self.translate_news(self.news_class(news))
        return (ent[0].name, news)

    def news_class(self, new):
        if (new > -0.5 and new < 0.5):
            return 0
        if (new > -1.5 and new < 1.5):
            if (new > 0):
                return 1
            else: return -1
        if (new > 0):
            return 2
        else: return -2

    def train(self):
        df = pd.DataFrame(data=self.dataset, columns=['Usuario', 'Empresa', 'Noticia', 'Investimento'])
        X = df.iloc[:,:-1]
        y = df.iloc[:,-1]
        self.knn.fit(X,y)

    def predict(self, perfil, num):
        r = dict()
        for i in range(num):
            data_pred = []
            comp, news = self.new_article()
            comp_lvl = self.get_ent_lvl(comp)
            data_pred += [perfil, comp_lvl, self.news_class(news)]
            pred = self.knn.predict([data_pred])
            r[comp] = self.translate_adv(int(pred[0]))
        return r

    def make_articles(self, num):
        for i in range(num):
            self.new_article()

    def translate_news(self, num):
        abc = dict({-2: 'muito ruim',
        -1: 'ruim',
        0: 'neutra',
        1: 'boa',
        2: 'muito boa'})
        return abc[num]

    def translate_adv(self, num):
        abc = dict({
        -1: 'Vender',
        0: 'Manter',
        1: 'Comprar'})
        return abc[num]

    def users(self):
        u = dict()
        for client in self.clients:
            u[client.name] = client.perfil
        return u

    def companys(self):
        c = dict()
        for comp in self.enterprises:
            c[comp.name] = comp.risk_lvl()
            # print(comp.name)
            # print(comp.risk_lvl())
        return c

    def get_ent_lvl(self, name):
        for ent in self.enterprises:
            if (ent.name == name):
                return ent.risk_lvl()
