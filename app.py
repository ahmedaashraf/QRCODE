from flask import Flask, request, render_template,send_file,Response # Importing flask features
from flask_cors import CORS, cross_origin
from flask_restplus import Api, Resource, fields # RestPlus adds swagger to flask and also the overriding of the APIs
from werkzeug.datastructures import FileStorage,ImmutableMultiDict
from werkzeug import secure_filename
from PIL import Image
import io
from generate import generate


import os
flask_app = Flask(__name__) # Initializting APP name


cors = CORS(flask_app,resources={r"*": {"origins": "*"}})


@flask_app.errorhandler(404) 
def not_found(e): 
	# Adding a 404 custom page
	return render_template("404.html") 

# Initializing app details for documentation
app = Api(app = flask_app, 
		  version = "1.0", 
		  title = "QRCODE GENERATOR", 
		  description = "An API which generates a qrcode with a logo")

# Adding the namespace as "spellcheck" for the API 
name_space = app.namespace('generate', description='Returns a QRCODE')

upload_parser = app.parser()
upload_parser.add_argument('size',location='args',required=True)
upload_parser.add_argument('link',location='args',required=True)
upload_parser.add_argument('file_image', location='files',
                           type=FileStorage, required=False)



# Initilizing the API route
@name_space.route("/api/v1.0/", methods=['POST','GET'])
class MainClass(Resource):
	# Defining the responses, params is the sentence to be checked!
	@app.doc(responses={ 200: 'OK', 400: 'Invalid Input'},params={ 'file_image': 'Include image file',"link":"Link","size":"qr code size" })
	@app.expect(upload_parser)
	def post(self): # the post method
		
		# Defining Request Parameters
		size = request.args.get("size")
		link = request.args.get("link")
		file_image = request.files.get('file_image')
		
		print(size)
		print(link)
		print(file_image)

		
		if file_image is not None:
			filename = secure_filename(file_image.filename)
			im = Image.open(file_image)
			qrcode = generate(link,im,size)
		
		else:
			qrcode = generate(link,None,size)
		
		
		output = io.BytesIO()
		qrcode.save(output, format='JPEG')  
		output.seek(0)
		response = Response
		response = send_file(output, as_attachment=True, attachment_filename="QRCODE.jpeg")
		response.headers.add('Access-Control-Allow-Origin', '*')
		response.headers.add('Access-Control-Allow-Methods', '*')
		response.headers.add('Access-Control-Allow-Headers', 'X-PINGOTHER')
		response.headers.add('Access-Control-Allow-Headers','Content-Type')
		response.headers.add('Access-Control-Max-Age', '86400')
		
		
		try:
			return response

   
		except KeyError as e:
			name_space.abort(500, e.__doc__, status = "Could not process the information", statusCode = "500")
		except Exception as e:
			name_space.abort(400, e.__doc__, status = "Could not process the information", statusCode = "400")

