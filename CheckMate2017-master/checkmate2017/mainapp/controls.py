def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def calculate_score(ch,points):
	if ch == '1':
		return(-20)
	elif ch == '2':
		return(points)
	elif ch == '3':
		return(-10)
	else:
		return(0)
