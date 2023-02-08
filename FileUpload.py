import jinja2
import os
import aiohttp_jinja2
from zipfile import ZipFile
from aiohttp import web

routes = web.RouteTableDef()

@routes.get('/')
async def Homepage(request):
    response = aiohttp_jinja2.render_template("index.html", request, context={})
    return response

@routes.post('/zip')
async def UploadFile(request):
    print("File Uploaded")
    temp = await request.post()
    get_file = temp['file'].file

    with ZipFile(get_file) as file:
        file_name = file.namelist()
        print(file_name)
        file.extractall(os.path.join(os.getcwd(),'save_file'))
        print("Succesfully Extracted!!!")
        file_name_dict = {'Name':file_name}
    response = aiohttp_jinja2.render_template("layout.html",request,context=file_name_dict)
    return response


app = web.Application()
aiohttp_jinja2.setup(app,loader=jinja2.FileSystemLoader('templates'))
app.add_routes(routes)
web.run_app(app)