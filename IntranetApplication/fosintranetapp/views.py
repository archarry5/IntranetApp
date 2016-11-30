# this was an empyt file. 
from django.http import HttpResponse
from django.views.generic.base import View


def HelloWorld(request):
    response_text = '<html>' + '<head>'+' <title>Greetings to the world</title>' +'</head>' +'<body>' +' <h1>Greetings to the world</h1>' +'<p>Hello, world!</p>' + '</body>' +'</html>'      
    return HttpResponse(response_text)
