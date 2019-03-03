class http_handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # parse request
        request = urllib.parse.urlparse(self.path)
        params = dict(urllib.parse.parse_qsl(request.query))
 
        # create response
        body = self.body(request.path, params)
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def body(self, request, params):
        response = '<html><header><title>sample</title><link rel="stylesheet" href="https://cdn.rawgit.com/alexanderGugel/papier/master/dist/papier-1.0.0.min.css"></header><body class="bg-subtle"><div style="width:50%;margin:0 auto">'
        if request == "/get":
            # 投稿用フォームを挿入
            response += '<section class="panel"><header>Post from:</header><main><form method="GET" action="/post"><input type="text" name="message" placeholder="message"><input type="submit" value="送信"></form></main></section>'
            # 投稿内容を表示
            for e in sorted(db.get(), key=lambda e: e[2], reverse=True):
                response += '<section class="panel"><header>{0}</header><main>{1}</main></section>'.format(time.strftime("%Y/%m/%d %H:%M:%S", time.localtime(e[2])), e[1])
        
        elif request == "/post":
            if not "message" in params:
                response += "<h1>Invalid Post</h1>"
            else:
                db.post(params["message"])
                response += '<meta http-equiv="REFRESH" content="1;URL=/get"><h1>Post Successed.</h1>'
 
        else:
            response += "<h1>Invalid Request</h1>"
 
        # フッター
        response += '</div></body></html>'
 
        return response.encode('utf-8')