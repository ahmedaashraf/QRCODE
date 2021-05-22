import qrcode

def generate(text,image,size):

	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_H,
		box_size=int(size),
		border=5
	)
	qr.add_data(text)
	qr.make(fit=True)
	img =qr.make_image(fill_color="black",back_color="white").convert('RGB')
	
	if image is not None:
		logo_display = image
		logo_display.thumbnail((60, 60))
		logo_pos = ((img.size[0]- logo_display.size[0])// 2, (img.size[1] -logo_display.size[1]) //2)
		img.paste(logo_display,logo_pos)
		
	return img
