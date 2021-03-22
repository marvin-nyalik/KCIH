from django.shortcuts import render
from django.http import *
from .templates import *
from .models import *
from passlib.hash import pbkdf2_sha256
from django.core.paginator import Paginator
from django.views.generic import View
from django.utils import timezone
from .models import *
from .render import Render
# Create your views here.

# Login functionality...
'''def login_render >> renders the login form
def authenticate_user >> checks the existence & validity of the user,

Creates a session object to mark the user session
'''
def login_render(request):
	return render(request, 'login.html', {})

def authenticate_user(request):
	if request.method == 'POST':
		idNumber = request.POST['idNo']
		password = request.POST['password']
		idNo = int(idNumber)

		try:
			user = Admin.objects.filter(idNo=idNo)[0]
			if user is not None:
				request.session['username'] = user.idNo
				if user.verify_password(password):
					return render(request, 'admin_welcome.html', {'user': user,})
		except:
			pass
		try:
			user = MP.objects.filter(idNo=idNo)[0]
			if user is not None:
				request.session['username'] = user.idNo
				if user.verify_password(password):
					return render(request, 'mp_start.html', {'user': user, })
		except:
			pass
		try:
			user = MCA.objects.filter(idNo=idNo)[0]
			if user is not None:
				request.session['username'] = user.idNo
				if user.verify_password(password):
					return render(request, 'mca_start.html', {'user': user,})
		except:
			pass
		try:
			user = MinistryOfficial.objects.filter(idNo=idNo)[0]
			if user is not None:
				request.session['username'] = user.idNo
				if user.verify_password(password):
					return render(request, 'min_start.html', {'user': user,})
		except:
			pass
		try:
			user = UnionOfficial.objects.filter(idNo=idNo)[0]
			if user is not None:
				request.session['username'] = user.idNo
				if user.verify_password(password):
					return render(request, 'union_start.html', {'user': user,})
		except:
			pass
		try:
			user = Leader.objects.filter(idNo=idNo)[0]
			if user is not None:
				request.session['username'] = user.idNo
				if user.verify_password(password):
					return render(request, 'leader_start.html', {'user': user, })
				else:
					alert = 'User does not exist'
					return render(request, '404.html', {'alert': alert,})
			        
		except:
			alert = 'User does not exist'
			return render(request, '404.html', {'alert': alert, })

#Log out functionality, Deletes the session, Redirects to start page
def logout(request):
	try:
		request.session.flush()
	except KeyError:
		pass
	return render(request, 'start.html')

'''Registration function by the junior system admin
def render_***_register to bring up the registration page for entity
***, eg leader, MP, etc...'''

def render_home_register(request):
	use = request.session['username']
	user = Admin.objects.filter(idNo=use)[0]
   
	return render(request, 'admin_reg_welcome.html', {'user': user,})

def render_leader_register(request):
	use = request.session['username']
	user = Admin.objects.filter(idNo=use)[0]
	pos = Position.objects.all()
	return render(request, 'admin_reg_leaders.html', {'positions': pos, 'user': user,})

def render_MP_register(request):
	use = request.session['username']
	user = Admin.objects.filter(idNo=use)[0]
	con = Constituency.objects.all()
	return render(request, 'admin_reg_mp.html', {'constituencies': con, 'user': user, })

def render_MCA_register(request):
	use = request.session['username']
	user = Admin.objects.filter(idNo=use)[0]
	war = Ward.objects.all()
	return render(request, 'admin_reg_mca.html', {'wards': war, 'user': user,})

def render_Min_Off_register(request):
	use = request.session['username']
	user = Admin.objects.filter(idNo=use)[0]
	mins = Ministry.objects.all()
	return render(request, 'admin_reg_min_off.html', {'ministries': mins, 'user': user,})

def render_Union_Off_register(request):
	use = request.session['username']
	user = Admin.objects.filter(idNo=use)[0]
	uni = Union.objects.all()
	return render(request, 'admin_reg_union_off.html', {'unions': uni, 'user': user, })

''' Actual registration process by the junior system admin'''
'''The following registers the users of the system
Considering all the factors such as the relationships between the entities eg. 

One constituency having only one MP, 
The county having only 1 senator etc etc'''


def register_leader(request):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		finame = request.POST['fname']
		liname = request.POST['lname']
		idNumber = request.POST['idNo']
		position = request.POST['position']
		image = request.FILES['pic']
		all_leaders = Leader.objects.all()
		pos = Position.objects.all()
		p = Position.objects.filter(position=position)[0]
		for a in all_leaders:
			if a.position == p:
				alert = "A leader with this position exists.."
				return render(request, 'admin_reg_leaders.html', {'user': admin,'alert': alert, 'positions': pos,})

		l = Leader()
		l.fname = finame
		l.lname = liname
		l.image = image
		l.idNo = int(idNumber)
		l.position = p
		l.password = pbkdf2_sha256.encrypt(idNumber, rounds=12000, salt_size = 32)
		l.save()
		alert = "Registration successful..."
		return render(request, '202.html', {'user': admin,'alert': alert,})
	else:
		alert ='Registration method not fulfilled'
		pos = Position.objects.all()
		return render(request, 'admin_reg_leaders.html', {'positions': pos, 'alert': alert})


def register_MP(request):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		finame = request.POST['fname']
		liname = request.POST['lname']
		idNumber = request.POST['idNo']
		con = request.POST['con']
		image = request.FILES['picture']
		all_mps = MP.objects.all()
		cons = Constituency.objects.all()
		c = Constituency.objects.filter(name=con)[0]
		for a in all_mps:
			if a.constituency == c:
				alert = "Constituency has an MP.."
				return render(request, 'admin_reg_mp.html', {'user': admin,'alert': alert, 'constituencies': cons,})

		l = MP()
		l.fname = finame
		l.lname = liname
		l.image = image
		l.idNo = int(idNumber)
		l.constituency = c
		l.password = pbkdf2_sha256.encrypt(idNumber, rounds=12000, salt_size = 32)
		l.save()
		alert = "Registration successful..."
		return render(request, '202.html', {'user': admin,'alert': alert,})
	else:
		alert ='Registration method not fulfilled...'
		cons = Constituency.objects.all()
		return render(request, 'admin_reg_mp.html', {'constituencies': cons, 'alert': alert})


def register_MCA(request):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		finame = request.POST['fname']
		liname = request.POST['lname']
		idNumber = request.POST['idNo']
		con = request.POST['ward']
		image = request.FILES['picture']
		all_mps = MCA.objects.all()
		cons = Ward.objects.all()
		c = Ward.objects.filter(name=con)[0]
		for a in all_mps:
			if a.ward == c:
				alert = "Ward has an MCA.."
				return render(request, 'admin_reg_mca.html', {'user': admin,'alert': alert, 'wards': cons,})

		l = MCA()
		l.fname = finame
		l.lname = liname
		l.image = image
		l.idNo = int(idNumber)
		l.ward = c
		l.password = pbkdf2_sha256.encrypt(idNumber, rounds=12000, salt_size = 32)
		l.save()
		alert = "Registration successful..."
		return render(request, '202.html', {'alert': alert, 'user': admin,})
	else:
		alert ='Registration method not fulfilled...'
		cons = Ward.objects.all()
		return render(request, 'admin_reg_mca.html', {'wards': cons, 'alert': alert})


def register_Min_Off(request):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		finame = request.POST['fname']
		liname = request.POST['lname']
		idNumber = request.POST['idNo']
		con = request.POST['ministry']
		image = request.FILES['picture']
		all_mps = MinistryOfficial.objects.all()
		cons = Ministry.objects.all()
		c = Ministry.objects.filter(name=con)[0]
		for a in all_mps:
			if a.ministry == c:
				alert = "Ministry has an official.."
				return render(request, 'admin_reg_min_off.html', {'alert': alert, 'ministries': cons, 'user': admin,})

		l = MinistryOfficial()
		l.fname = finame
		l.lname = liname
		l.image = image
		l.idNo = int(idNumber)
		l.ministry = c
		l.password = pbkdf2_sha256.encrypt(idNumber, rounds=12000, salt_size = 32)
		l.save()
		alert = "Registration successful..."
		return render(request, '202.html', {'user': admin,'alert': alert,})
	else:
		alert ='Registration method not fulfilled...'
		cons = Ministry.objects.all()
		return render(request, 'admin_reg_min_off.html', {'ministries': cons, 'alert': alert})

def register_Union_Off(request):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		finame = request.POST['fname']
		liname = request.POST['lname']
		idNumber = request.POST['idNo']
		con = request.POST['union']
		image = request.FILES['picture']
		all_mps = UnionOfficial.objects.all()
		cons = Union.objects.all()
		c = Union.objects.filter(name=con)[0]
		for a in all_mps:
			if a.union == c:
				alert = "Union has an official.."
				return render(request, 'admin_reg_union_off.html', {'user': admin,'alert': alert, 'unions': cons,})

		l = UnionOfficial()
		l.fname = finame
		l.lname = liname
		l.image = image
		l.idNo = int(idNumber)
		l.union = c
		l.password = pbkdf2_sha256.encrypt(idNumber, rounds=12000, salt_size = 32)
		l.save()
		alert = "Registration successful..."
		return render(request, '202.html', {'user': admin,'alert': alert,})
	else:
		alert ='Registration method not fulfilled...'
		cons = Union.objects.all()
		return render(request, 'admin_reg_union_off.html', {'unions': cons, 'alert': alert})


#End of Registration function methods

#Admin password Reset
'''The individual methods e.g def reset_*** were written to reduce
the complexity of the program due to the underlying database structure.

These methods of the form def reset_*** resets the password of the 

entities to the original ID NUMBER'''

def reset_leader(request, pk):
	leader = Leader.objects.get(id=pk)
	leader.password = pbkdf2_sha256.encrypt(str(leader.idNo))
	alert = "Password reset successful for idNumber"
	return render(request, '203.html', {'alert': alert, 'leader': leader,})


def reset_mp(request, pk):
	leader = MP.objects.get(id=pk)
	leader.password = pbkdf2_sha256.encrypt(str(leader.idNo))
	alert = "Password reset successful for idNumber"
	return render(request, '203.html', {'alert': alert, 'leader': leader,})


def reset_mca(request, pk):
	leader = MCA.objects.get(id=pk)
	leader.password = pbkdf2_sha256.encrypt(str(leader.idNo))
	alert = "Password reset successful for idNumber"
	return render(request, '203.html', {'alert': alert, 'leader': leader,})


def reset_ministry(request, pk):
	leader = MinistryOfficial.objects.get(id=pk)
	leader.password = pbkdf2_sha256.encrypt(str(leader.idNo))
	alert = "Password reset successful for idNumber"
	return render(request, '203.html', {'alert': alert, 'leader': leader,})


def reset_union(request, pk):
	leader = UnionOfficial.objects.get(id=pk)
	leader.password = pbkdf2_sha256.encrypt(str(leader.idNo))
	alert = "Password reset successful for idNumber"
	return render(request, '203.html', {'alert': alert, 'leader': leader,})
'''USER MANAGEMENT
Allows the junior admin to view the user status and 
perform password management 
These methods def manage_*** displays the page for the management process..'''

def manage_home(request):
	user = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'manage_welcome.html', {'user': user,})

def manage_leaders(request):
	leaders = Leader.objects.all()
	user = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'upd_leader.html', {'county_leaders': leaders, 'user': user})

def manage_mps(request):
	leaders = MP.objects.all()
	user = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'upd_mp.html', {'county_leaders': leaders, 'user': user})


def manage_mcas(request):
	leaders = MCA.objects.all()
	user = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'upd_mca.html', {'county_leaders': leaders, 'user': user})

def manage_mins(request):
	leaders = MinistryOfficial.objects.all()
	user = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'upd_min.html', {'county_leaders': leaders, 'user': user})

def manage_unions(request):
	leaders = UnionOfficial.objects.all()
	user = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'upd_union.html', {'county_leaders': leaders, 'user': user})

#End of User management methods...

def render_leader_update(request):
	user = Leader.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'update_leader.html', {'user':user, })

def create_update(request):
	idNumber = request.session['username']
	print(idNumber)
	leader = Leader.objects.filter(idNo=int(idNumber))[0]
	print(leader)

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		image = request.FILES['image']

		up = LeaderUpdates()
		up.title = title
		up.message = message
		up.leader = leader
		up.location = location
		up.image = image
		up.save()
		alert = 'Update was successful..'
		return render(request, 'update_g.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


def render_mp_update(request):
	user = MP.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'update_mp.html', {'user':user, })

def create_MP_update(request):
	idNumber = request.session['username']
	leader = MP.objects.filter(idNo=int(idNumber))[0]
	

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		image = request.FILES['image']

		up = MPUpdates()
		up.title = title
		up.message = message
		up.mp = leader
		up.location = location
		up.image = image
		up.save()
		alert = 'Update was successful..'
		return render(request, 'update_go.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


def render_mca_update(request):
	user = MCA.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'update_mca.html', {'user':user, })

def create_MCA_update(request):
	idNumber = request.session['username']
	leader = MCA.objects.filter(idNo=int(idNumber))[0]
	

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		image = request.FILES['image']

		up = MCAUpdates()
		up.title = title
		up.message = message
		up.mca = leader
		up.location = location
		up.image = image
		up.save()
		alert = 'Update was successful..'
		return render(request, 'update_g_mca.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


def render_ministry_update(request):
	user = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'update_ministry.html', {'user':user, })

def create_MIN_update(request):
	idNumber = request.session['username']
	leader = MinistryOfficial.objects.filter(idNo=int(idNumber))[0]
	

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		image = request.FILES['image']

		up = MinistryUpdates()
		up.title = title
		up.message = message
		up.ministry = leader.ministry
		up.location = location
		up.image = image
		up.save()
		alert = 'Update was successful..'
		return render(request, 'update_g_min.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')
	

def render_union_update(request):
	user = UnionOfficial.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'update_union.html', {'user':user, })

def create_UNION_update(request):
	idNumber = request.session['username']
	leader = UnionOfficial.objects.filter(idNo=int(idNumber))[0]
	

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		image = request.FILES['image']

		up = UnionUpdates()
		up.title = title
		up.message = message
		up.union = leader.union
		up.location = location
		up.image = image
		up.save()
		alert = 'Update was successful..'
		return render(request, 'update_g_union.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')
#UPDATES: Rendering the form...
# def create_update(request):
# 	return render(request, 'create_update.html')

'''PROJECTS, creation & page render'''
def render_leader_project(request):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'create_project.html', {'user': leader,})

def create_leader_project(request):
	idNumber = request.session['username']
	leader = Leader.objects.filter(idNo=int(idNumber))[0]

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		estimate = int(request.POST['estimate'])
		image = request.FILES['image']
		allocated = int(request.POST['allocation'])
		des = request.POST['message']

		if allocated > estimate:
			alert = 'Allocation can not exceed estimate...'
			return render(request, 'create_project.html', {'alert': alert, 'user': leader,})

		up = LeaderProject()
		up.title = title
		up.message = message
		up.leader = leader
		up.location = location
		up.estimate = estimate
		des = request.POST['message']
		up.description = des
		up.allocation = allocated
		if image is not None:
			up.image = image
		else:
			up.image = None
		up.save()
		alert = 'Project registration successful..'
		return render(request, 'update_g.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


#MP projects
def render_mp_project(request):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'create_mp_project.html', {'user': leader,})

def create_mp_project(request):
	idNumber = request.session['username']
	leader = MP.objects.filter(idNo=int(idNumber))[0]

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		estimate = int(request.POST['estimate'])
		image = request.FILES['image']
		allocated = int(request.POST['allocation'])

		if allocated > estimate:
			alert = 'Allocation can not exceed estimate...'
			return render(request, 'create_mp_project.html', {'alert': alert, 'user': leader,})

		up = MPProject()
		up.title = title
		up.message = message
		up.mp = leader
		up.location = location
		up.estimate = estimate
		des = request.POST['message']
		up.description = des
		up.allocation = allocated
		if image is not None:
			up.image = image
		else:
			up.image = None
		up.save()
		alert = 'Project registration successful..'
		return render(request, 'update_go.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


def render_mca_project(request):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'create_mca_project.html', {'user': leader,})

def create_mca_project(request):
	idNumber = request.session['username']
	leader = MCA.objects.filter(idNo=int(idNumber))[0]

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		estimate = int(request.POST['estimate'])
		image = request.FILES['image']
		allocated = int(request.POST['allocation'])

		if allocated > estimate:
			alert = 'Allocation can not exceed estimate...'
			return render(request, 'create_mca_project.html', {'alert': alert, 'user': leader,})

		up = MCAProject()
		up.title = title
		up.message = message
		up.mca = leader
		up.location = location
		des = request.POST['message']
		up.description = des
		up.estimate = estimate
		up.allocation = allocated
		if image is not None:
			up.image = image
		else:
			up.image = None
		up.save()
		alert = 'Project registration successful..'
		return render(request, 'update_g_mca.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


def render_ministry_project(request):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'create_min_proj.html', {'user': leader,})

def create_ministry_project(request):
	idNumber = request.session['username']
	leader = MinistryOfficial.objects.filter(idNo=int(idNumber))[0]

	if request.method == 'POST':
		title = request.POST['title']
		message = request.POST['message']
		location = request.POST['location']
		estimate = int(request.POST['estimate'])
		image = request.FILES['image']
		des = request.POST['message']
		
		allocated = int(request.POST['allocation'])

		if allocated > estimate:
			alert = 'Allocation can not exceed estimate...'
			return render(request, 'create_min_proj.html', {'alert': alert, 'user': leader,})

		up = MinistryProject()
		up.title = title
		up.description = des
		up.message = message
		up.ministry = leader.ministry
		up.location = location
		up.estimate = estimate
		up.allocation = allocated
		if image is not None:
			up.image = image
		else:
			up.image = None
		up.save()
		alert = 'Project registration successful..'
		return render(request, 'update_g_min.html', {'alert': alert, 'user': leader, })
	return HttpResponse('Done..')


#MY UPDATES/PROJECTS
def my_leader_updates(request):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	updates = LeaderUpdates.objects.filter(leader=leader)
	#paginator = Paginator(updates, 6)
	all_updates = len(updates)
	#page = request.GET.get('page')
	#contacts = paginator.get_page(page)
    
	return render(request, 'my_updates.html', {'user': leader,
	 'total': all_updates, 'my_updates': updates, })

def my_leader_projects(request):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	updates = LeaderProject.objects.filter(leader=leader)
	count = 0
	n_count = 0
	for p in updates:
		if p.status:
			count += 1
		else:
			n_count += 1
	#paginator = Paginator(updates, 6)
	all_updates = len(updates)
	#page = request.GET.get('page')
	#contacts = paginator.get_page(page)
    
	return render(request, 'my_projects.html', {'user': leader,
	 'total': all_updates, 'my_projects': updates, 'total_comp': count,
	 'total_incomp': n_count, })


def my_mp_projects(request):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	updates = MPProject.objects.filter(mp=leader)
	count = 0
	n_count = 0
	for p in updates:
		if p.status:
			count += 1
		else:
			n_count += 1
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	# page = request.GET.get('page')
	# contacts = paginator.get_page(page)
    
	return render(request, 'my_mp_projects.html', {'user': leader,
	 'total': all_updates, 'my_projects': updates, 'total_comp': count,
	 'total_incomp': n_count, })

def my_mca_projects(request):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	updates = MCAProject.objects.filter(mca=leader)
	count = 0
	n_count = 0
	for p in updates:
		if p.status:
			count += 1
		else:
			n_count += 1
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	# page = request.GET.get('page')
	# contacts = paginator.get_page(page)
    
	return render(request, 'my_mca_projects.html', {'user': leader,
	 'total': all_updates, 'my_projects': updates, 'total_comp': count,
	 'total_incomp': n_count, })


def my_ministry_projects(request):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	updates = MinistryProject.objects.filter(ministry=leader.ministry)
	count = 0
	n_count = 0
	for p in updates:
		if p.status:
			count += 1
		else:
			n_count += 1
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	# page = request.GET.get('page')
	# contacts = paginator.get_page(page)
    
	return render(request, 'my_min_projects.html', {'user': leader,
	 'total': all_updates, 'my_projects': updates, 'total_comp': count,
	 'total_incomp': n_count, })


def lead_proj_complete(request, pk):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	proj = LeaderProject.objects.get(id=pk)
	proj.status = True
	proj.save()
	alert = 'Project marked as complete..'
	return render(request, 'update_g.html', {'p': proj, 'user': leader,'alert': alert, })

def mp_proj_complete(request, pk):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	proj = MPProject.objects.get(id=pk)
	proj.status = True
	proj.save()
	alert = 'Project marked as complete..'
	return render(request, 'update_go.html', {'p': proj, 'user': leader,'alert': alert, })

def mca_proj_complete(request, pk):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	proj = MCAProject.objects.get(id=pk)
	proj.status = True
	proj.save()
	alert = 'Project marked as complete..'
	return render(request, 'update_g_mca.html', {'p': proj, 'user': leader,'alert': alert, })


def min_proj_complete(request, pk):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	proj = MinistryProject.objects.get(id=pk)
	proj.status = True
	proj.save()
	alert = 'Project marked as complete..'
	return render(request, 'update_g_min.html', {'p': proj, 'user': leader,'alert': alert, })	

#UPDATING THE CONTENTS OF A PROJECT
'''INPUT SESSION USER OBJECT, AUTOMATIC PRIMARY KEY OF THE PROJECT'''
def lead_proj_update(request, pk):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	proj = LeaderProject.objects.get(id=pk)
	return render(request, 'update_leader_proj.html', {'p': proj, 'user': leader, })

def proj_update(request, pk):
	proj = LeaderProject.objects.get(id=pk)
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	prev = proj.allocation
	if request.method=='POST':
		message = request.POST['message']
		allocation = int(request.POST['allocation'])
		image = request.FILES['image']
		proj.message = message
		proj.image = image
		if prev > allocation:
			alert = 'Previous allocation cant be more than current allocation..'
			return render(request, 'update_leader_proj.html', {'p': proj, 'user': leader,})
		elif allocation > proj.estimate:
			alert = 'Allocation cant exceed estimate'
			return render(request, 'update_leader_proj.html', {'p': proj, 'user': leader,})
		else:
			proj.allocation = allocation
			proj.save()
			alert = 'Project update successful...'
			return render(request, 'update_g.html', {'alert': alert, 'user': leader, })


def MP_proj_update(request, pk):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	proj = MPProject.objects.get(id=pk)
	return render(request, 'update_mp_project.html', {'p': proj, 'user': leader, })

def MPproj_update(request, pk):
	proj = MPProject.objects.get(id=pk)
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	prev = proj.allocation
	if request.method=='POST':
		message = request.POST['message']
		allocation = int(request.POST['allocation'])
		image = request.FILES['image']
		proj.message = message
		proj.image = image
		if prev > allocation:
			alert = 'Previous allocation cant be more than current allocation..'
			return render(request, 'update_mp_project.html', {'p': proj, 'user': leader,})
		elif allocation > proj.estimate:
			alert = 'Allocation cant exceed estimate'
			return render(request, 'update_mp_project.html', {'p': proj, 'user': leader,})
		else:
			proj.allocation = allocation
			proj.save()
			alert = 'Project update successful...'
			return render(request, 'update_go.html', {'alert': alert, 'user': leader, })


def MCA_proj_update(request, pk):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	proj = MCAProject.objects.get(id=pk)
	return render(request, 'update_mca_project.html', {'p': proj, 'user': leader, })

def MCAproj_update(request, pk):
	proj = MCAProject.objects.get(id=pk)
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	prev = proj.allocation
	if request.method=='POST':
		message = request.POST['message']
		allocation = int(request.POST['allocation'])
		image = request.FILES['image']
		proj.message = message
		proj.image = image
		if prev > allocation:
			alert = 'Previous allocation cant be more than current allocation..'
			return render(request, 'update_mca_project.html', {'p': proj, 'user': leader,})
		elif allocation > proj.estimate:
			alert = 'Allocation cant exceed estimate'
			return render(request, 'update_mca_project.html', {'p': proj, 'user': leader,})
		else:
			proj.allocation = allocation
			proj.save()
			alert = 'Project update successful...'
			return render(request, 'update_g_mca.html', {'alert': alert, 'user': leader, })


def MIN_proj_update(request, pk):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	proj = MinistryProject.objects.get(id=pk)
	return render(request, 'update_ministry_project.html', {'p': proj, 'user': leader, })

def MINproj_update(request, pk):
	proj = MinistryProject.objects.get(id=pk)
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	prev = proj.allocation
	if request.method=='POST':
		message = request.POST['message']
		allocation = int(request.POST['allocation'])
		image = request.FILES['image']
		proj.message = message
		proj.image = image
		if prev > allocation:
			alert = 'Previous allocation cant be more than current allocation..'
			return render(request, 'update_ministry_project.html', {'p': proj, 'user': leader,})
		elif allocation > proj.estimate:
			alert = 'Allocation cant exceed estimate'
			return render(request, 'update_ministry_project.html', {'p': proj, 'user': leader,})
		else:
			proj.allocation = allocation
			proj.save()
			alert = 'Project update successful...'
			return render(request, 'update_g_min.html', {'alert': alert, 'user': leader, })

def my_MP_updates(request):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	updates = MPUpdates.objects.filter(mp=leader)
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	#page = request.GET.get('page')
	#contacts = paginator.get_page(page)
    
	return render(request, 'my_mp_updates.html', {'user': leader,
	 'total': all_updates, 'my_updates': updates, })



def my_MCA_updates(request):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	updates = MCAUpdates.objects.filter(mca=leader)
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	#page = request.GET.get('page')
	#contacts = paginator.get_page(page)
    
	return render(request, 'my_mca_updates.html', {'user': leader,
	 'total': all_updates, 'my_updates': updates, })


def my_Ministry_updates(request):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	updates = MinistryUpdates.objects.filter(ministry=leader.ministry)
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	# page = request.GET.get('page')
	# contacts = paginator.get_page(page)
    
	return render(request, 'my_min_updates.html', {'user': leader,
	 'total': all_updates, 'my_updates': updates, })


def my_Union_updates(request):
	leader = UnionOfficial.objects.filter(idNo=request.session['username'])[0]
	updates = UnionUpdates.objects.filter(union=leader.union)
	#paginator = Paginator(updates, 1)
	all_updates = len(updates)
	#page = request.GET.get('page')
	#contacts = paginator.get_page(page)
    
	return render(request, 'my_uni_updates.html', {'user': leader,
	 'total': all_updates, 'my_updates': updates, })


#USER PASSWORD CHANGE

def render_password_change(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'change-pwd.html', {'user':leader, })

def change_password(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		password = request.POST['pass']
		enc = pbkdf2_sha256.encrypt(password)
		print(enc)
		new_pass = request.POST['newpass']
		con_pass = request.POST['connewpass']
        
		if leader.verify_password(password):
			if new_pass == con_pass:
				enc_pwd = pbkdf2_sha256.encrypt(new_pass)
				leader.password = enc_pwd
				leader.save()
				alert = 'Password change successful..'
				return render(request, 'change-pwd.html', {'alert': alert, 'user': leader, })
				print(alert)
			else:
				alert = 'New passwords do not match..'
				return render(request, 'change-pwd.html', {'alert': alert, 'user': leader, })


def render_mp_password_change(request):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'MPchange_pwd.html', {'user':leader, })

def MPchange_password(request):
	leader = MP.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		password = request.POST['pass']
		new_pass = request.POST['newpass'].strip()
		con_pass = request.POST['connewpass'].strip()
        
		if leader.verify_password(password):
			if new_pass == con_pass:
				enc_pwd = pbkdf2_sha256.encrypt(new_pass)
				leader.password = enc_pwd
				leader.save()
				alert = 'Password change successful..'
				return render(request, 'MPchange_pwd.html', {'alert': alert, 'user': leader, })
				print(alert)
			else:
				alert = 'New passwords do not match..'
				return render(request, 'MPchange_pwd.html', {'alert': alert, 'user': leader, })


def render_mca_password_change(request):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'MCAchange_pwd.html', {'user':leader, })

def MCAchange_password(request):
	leader = MCA.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		password = request.POST['pass']
		new_pass = request.POST['newpass'].strip()
		con_pass = request.POST['connewpass'].strip()
        
		if leader.verify_password(password):
			if new_pass == con_pass:
				enc_pwd = pbkdf2_sha256.encrypt(new_pass)
				leader.password = enc_pwd
				leader.save()
				alert = 'Password change successful..'
				return render(request, 'MCAchange_pwd.html', {'alert': alert, 'user': leader, })
				print(alert)
			else:
				alert = 'New passwords do not match..'
				return render(request, 'MCAchange_pwd.html', {'alert': alert, 'user': leader, })

def render_min_password_change(request):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'MINchange_pwd.html', {'user':leader, })

def MINchange_password(request):
	leader = MinistryOfficial.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		password = request.POST['pass']
		new_pass = request.POST['newpass'].strip()
		con_pass = request.POST['connewpass'].strip()
        
		if leader.verify_password(password):
			if new_pass == con_pass:
				enc_pwd = pbkdf2_sha256.encrypt(new_pass)
				leader.password = enc_pwd
				leader.save()
				alert = 'Password change successful..'
				return render(request, 'MINchange_pwd.html', {'alert': alert, 'user': leader, })
				print(alert)
			else:
				alert = 'New passwords do not match..'
				return render(request, 'MINchange_pwd.html', {'alert': alert, 'user': leader, })


def render_union_password_change(request):
	leader = UnionOfficial.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'UNIchange_pwd.html', {'user':leader, })

def UNIONchange_password(request):
	leader = UnionOfficial.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		password = str(request.POST['pass'])
		new_pass = str(request.POST['newpass'].strip())
		print(new_pass)
		con_pass = str(request.POST['connewpass'].strip())
		print(con_pass)
		print(new_pass==con_pass)
		print(leader.verify_password(password))
        
		if leader.verify_password(password):
			if new_pass == con_pass:
				enc_pwd = pbkdf2_sha256.encrypt(new_pass)
				print(leader.password)
				leader.password = None
				print('done')
				leader.password = enc_pwd
				leader.save()
				print(leader.password)
				alert = 'Password change successful..'
				return render(request, 'UNIchange_pwd.html', {'alert': alert, 'user': leader, })

			else:
				alert = 'New passwords do not match. Re-enter to retry.'
				return render(request, 'UNIchange_pwd.html', {'alert': alert, 'user': leader, })
	            
	 		
	return HttpResponse('Done')


def Lrender_password_change(request):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'Lchange_pwd.html', {'user':leader, })

def Lchange_password(request):
	leader = Leader.objects.filter(idNo=request.session['username'])[0]
	if request.method == 'POST':
		password = request.POST['pass']
		enc = pbkdf2_sha256.encrypt(password)
		print(enc)
		new_pass = request.POST['newpass']
		con_pass = request.POST['connewpass']
        
		if leader.verify_password(password):
			if new_pass == con_pass:
				enc_pwd = pbkdf2_sha256.encrypt(new_pass)
				leader.password = enc_pwd
				leader.save()
				alert = 'Password change successful..'
				return render(request, 'Lchange_pwd.html', {'alert': alert, 'user': leader, })
				print(alert)
			else:
				alert = 'New passwords do not match. Re-enter to retry.'
				return render(request, 'Lchange_pwd.html', {'alert': alert, 'user': leader, })


#ARCHIVES
def archive_home(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	return render(request, 'archive_start.html', {'user': leader, })

def archive_mp_render(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	mps = MP.objects.all()
	return render(request, 'archive_mp.html', {'user': leader,'county_leaders': mps, })

def archive_mp(request, pk):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	leader = MP.objects.get(id=pk)
	proj = MPProject.objects.filter(mp=leader)
	updates = MPUpdates.objects.filter(mp=leader)

	for p in proj:
		a = MPProjArchive()
		a.title = p.title
		a.estimate = p.estimate
		a.allocation = p.allocation
		a.location = p.location
		a.status = p.status
		a.save()
	    
	proj.delete()

	for u in updates:
		up = MPUpdArchive()
		up.sponsor = u.mp
		up.title = u.title
		up.message = u.message
		up.day = u.day
		
		up.save()
	updates.delete()
	leader.delete()

	alert = 'MP projects and updates added to archives...'

	return render(request, 'archive_ack.html', {'alert': alert, 'user': admin, } )


def archive_leader_render(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	mps = Leader.objects.all()
	return render(request, 'archive_leaders.html', {'user': leader,'county_leaders': mps, })

def archive_leader(request, pk):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	leader = Leader.objects.get(id=pk)
	proj = LeaderProject.objects.filter(leader=leader)
	updates = LeaderUpdates.objects.filter(leader=leader)

	for p in proj:
		a = LeaderProjArchive()
		a.title = p.title
		a.sponsor = p.leader
		a.estimate = p.estimate
		a.allocation = p.allocation
		a.location = p.location
		a.status = p.status
		a.save()
	    
	proj.delete()

	for u in updates:
		up = LeaderUpdArchive()
		up.sponsor = u.leader
		up.title = u.title
		up.message = u.message
		up.day = u.day
		
		up.save()
	updates.delete()
	leader.delete()

	alert = 'This leader and his projects and updates have been added to archives...'

	return render(request, 'archive_ack.html', {'alert': alert, 'user': admin, } )


def archive_mca_render(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	mps = MCA.objects.all()
	return render(request, 'archive_mca.html', {'user': leader,'county_leaders': mps, })

def archive_mca(request, pk):
	admin = Admin.objects.filter(idNo=request.session['username'])[0]
	leader = MCA.objects.get(id=pk)
	proj = MCAProject.objects.filter(mca=leader)
	updates = MCAUpdates.objects.filter(mca=leader)

	for p in proj:
		a = MCAProjArchive()
		a.title = p.title
		a.sponsor = p.mca
		a.estimate = p.estimate
		a.allocation = p.allocation
		a.location = p.location
		a.status = p.status
		a.save()
	    
	proj.delete()

	for u in updates:
		up = MCAUpdArchive()
		up.sponsor = u.mca
		up.title = u.title
		up.message = u.message
		up.day = u.day
		
		up.save()
	updates.delete()
	leader.delete()

	alert = 'This leader and his projects and updates have been added to archives...'

	return render(request, 'archive_ack.html', {'alert': alert, 'user': admin, } )


#REPORTS MODULE...YEEEEY
'''BEcause no system is valid without a report'''

def report_home(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	return render (request, 'report_start.html', {'user': leader, })

def report_init(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	return render (request, 'report_init.html', {'user': leader, })


def leader_report(request):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	c_leaders = Leader.objects.all()
	mps = MP.objects.all()
	mcas = MCA.objects.all()
	ministries = Ministry.objects.all()
	unions = Union.objects.all()
	return render (request, 'projects_report.html', 
		{'user': leader, 
		'leaders': c_leaders,
		'mps': mps,
		'mcas': mcas,
		'min': ministries,
		'unions': unions,})


def LeaderReport(request, pk):
	leader = Admin.objects.filter(idNo=request.session['username'])[0]
	lead = Leader.objects.get(id=pk)
	proj = LeaderProject.objects.filter(leader=lead)
	count = len(proj)
	comp, incomp = 0
	for p in proj:
		if status:
			comp += 1
		else:
			incomp += 1

class Pdf(View):

    def get(self, request, pk):
	    leader = Admin.objects.filter(idNo=request.session['username'])[0]
	    lead = Leader.objects.get(id=pk)
	    proj = LeaderProject.objects.filter(leader=lead)
	    upd = LeaderUpdates.objects.filter(leader=lead)
	    today = timezone.now()
	    count = len(proj)
	    num = len(upd)
	    comp = 0
	    incomp = 0
	    estimates = 0
	    allocation = 0
	    for p in proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    return Render.render('leader_project_pdf.html', {
		'count':count,
            'today': today,
            'updates': upd,
            'num': num,
            'estimate': estimates,
            'allocation': allocation,
            'proj': proj,
            'lead':lead,
            'leader':leader,
            'complete': comp,
            'incomplete':incomp,
            'request': request
        })

#MP REPORTS
class MpPdf(View):

    def get(self, request, pk):
	    leader = Admin.objects.filter(idNo=request.session['username'])[0]
	    lead = MP.objects.get(id=pk)
	    proj = MPProject.objects.filter(mp=lead)
	    upd = MPUpdates.objects.filter(mp=lead)
	    today = timezone.now()
	    count = len(proj)
	    num = len(upd)
	    comp = 0
	    incomp = 0
	    estimates = 0
	    allocation = 0
	    for p in proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    return Render.render('mp_projects_pdf.html', {
		'count':count,
            'today': today,
            'updates': upd,
            'num': num,
            'estimate': estimates,
            'allocation': allocation,
            'proj': proj,
            'lead':lead,
            'leader':leader,
            'complete': comp,
            'incomplete':incomp,
            'request': request
        })

	
class McaPdf(View):

    def get(self, request, pk):
	    leader = Admin.objects.filter(idNo=request.session['username'])[0]
	    lead = MCA.objects.get(id=pk)
	    proj = MCAProject.objects.filter(mca=lead)
	    upd = MCAUpdates.objects.filter(mca=lead)
	    today = timezone.now()
	    count = len(proj)
	    num = len(upd)
	    comp = 0
	    incomp = 0
	    estimates = 0
	    allocation = 0
	    for p in proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    return Render.render('mca_projects_pdf.html', {
		'count':count,
            'today': today,
            'updates': upd,
            'num': num,
            'estimate': estimates,
            'allocation': allocation,
            'proj': proj,
            'lead':lead,
            'leader':leader,
            'complete': comp,
            'incomplete':incomp,
            'request': request
        })

class MinPdf(View):

    def get(self, request, pk):
	    leader = Admin.objects.filter(idNo=request.session['username'])[0]
	    lead = Ministry.objects.get(id=pk)
	    proj = MinistryProject.objects.filter(ministry=lead)
	    upd = MinistryUpdates.objects.filter(ministry=lead)
	    today = timezone.now()
	    count = len(proj)
	    num = len(upd)
	    comp = 0
	    incomp = 0
	    estimates = 0
	    allocation = 0
	    for p in proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    return Render.render('min_projects_pdf.html', {
		'count':count,
            'today': today,
            'updates': upd,
            'num': num,
            'estimate': estimates,
            'allocation': allocation,
            'proj': proj,
            'lead':lead,
            'leader':leader,
            'complete': comp,
            'incomplete':incomp,
            'request': request
        })

class ProjectsPdf(View):

    def get(self, request):
	    leader = Admin.objects.filter(idNo=request.session['username'])[0]
	    lead_projects = LeaderProject.objects.all()
	    mp_proj = MPProject.objects.all()
	    mca_proj = MCAProject.objects.all()
	    min_proj = MinistryProject.objects.all()
	    today = timezone.now()
	    count = len(lead_projects) + len(mp_proj) + len(mca_proj) + len(min_proj)
	    comp = 0
	    incomp = 0
	    estimates = 0
	    allocation = 0
	    for p in mp_proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    for p in mca_proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    for p in min_proj:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1

	    for p in lead_projects:
	    	estimates += p.estimate
	    	allocation += p.allocation

	    	if p.status:
	    		comp += 1
	    	else:
	    		incomp += 1


	    return Render.render('all_projects_pdf.html', {
		'count':count,
            'today': today,
            'estimate': estimates,
            'allocation': allocation,
            'mp_proj': mp_proj,
            'mca_proj': mca_proj,
            'min_proj': min_proj,
            'lead_projects':lead_projects,
            'leader':leader,
            'complete': comp,
            'incomplete':incomp,
            'request': request
        })


class UpdatesPdf(View):

    def get(self, request):
	    leader = Admin.objects.filter(idNo=request.session['username'])[0]
	    lead_projects = LeaderUpdates.objects.all()
	    mp_proj = MPUpdates.objects.all()
	    mca_proj = MCAUpdates.objects.all()
	    min_proj = MinistryUpdates.objects.all()
	    today = timezone.now()
	    count = len(lead_projects) + len(mp_proj) + len(mca_proj) + len(min_proj)
	   
	    return Render.render('all_updates_pdf.html', {
		'count':count,
            'today': today,
            'mp_proj': mp_proj,
            'mca_proj': mca_proj,
            'min_proj': min_proj,
            'lead_projects':lead_projects,
            'leader':leader,
            'request': request
        })


#PUBLIC RENDERING
def public_leader(request):
	leaders = Leader.objects.all()
	mps = MP.objects.all()
	mcas = MCA.objects.all()

	unions = Union.objects.all()
	mins = Ministry.objects.all()

	return render(request, 'leaders.html', {'county_mcas': mcas,
		'county_mps': mps, 'county_leaders': leaders, "county_unions": unions, 'county_ministries': mins,})

def public_unions(request):
	leaders = Leader.objects.all()
	unions = Union.objects.all()
	mins = Ministry.objects.all()

	return render(request, 'unions.html', { 'county_leaders': leaders, 'county_unions': unions,
	 'county_ministries': mins,})


def public_ministry(request):
	leaders = Leader.objects.all()
	unions = Union.objects.all()
	mins = Ministry.objects.all()

	return render(request, 'ministries.html', {
		 'county_leaders': leaders, 'county_unions': unions,
		 'county_ministries': mins,})


def county_updates(request, pk):
	leader = Leader.objects.get(id=pk)
	county_leaders = Leader.objects.exclude(id=pk)
	today = timezone.now()
	updates = LeaderUpdates.objects.filter(leader=leader)

	return render(request, 'county_detail.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def county_ext(request, pk):
	update = LeaderUpdates.objects.get(id=pk)
	other = LeaderUpdates.objects.exclude(id=pk)
	leaders = Leader.objects.all()

	today = timezone.now()
	return render(request, 'county_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })

def county_proj(request, pk):
	leader = Leader.objects.get(id=pk)
	county_leaders = Leader.objects.all()
	today = timezone.now()
	updates = LeaderProject.objects.filter(leader=leader)

	return render(request, 'county_projects.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def county_ext_proj(request, pk):
	update = LeaderProject.objects.get(id=pk)
	other = LeaderProject.objects.exclude(id=pk)
	leaders = Leader.objects.all()

	today = timezone.now()
	return render(request, 'county_proj_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })

def mp_updates(request, pk):
	leader = MP.objects.get(id=pk)
	county_leaders = MP.objects.exclude(id=pk)
	today = timezone.now()
	updates = MPUpdates.objects.filter(mp=leader)

	return render(request, 'mp_details.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def mp_ext(request, pk):
	update = MPUpdates.objects.get(id=pk)
	other = MPUpdates.objects.exclude(id=pk)
	leaders = MP.objects.all()

	today = timezone.now()
	return render(request, 'mp_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })


def mp_proj(request, pk):
	leader = MP.objects.get(id=pk)
	county_leaders = MP.objects.all()
	today = timezone.now()
	updates = MPProject.objects.filter(mp=leader)

	return render(request, 'mp_projects.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def mp_ext_proj(request, pk):
	update = MPProject.objects.get(id=pk)
	other = MPProject.objects.exclude(id=pk)
	leaders = MP.objects.all()

	today = timezone.now()
	return render(request, 'mp_proj_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })


def mca_updates(request, pk):
	leader = MCA.objects.get(id=pk)
	county_leaders = MCA.objects.exclude(id=pk)
	today = timezone.now()
	updates = MCAUpdates.objects.filter(mca=leader)

	return render(request, 'mca_details.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def mca_ext(request, pk):
	update = MCAUpdates.objects.get(id=pk)
	other = MCAUpdates.objects.exclude(id=pk)
	leaders = MCA.objects.all()

	today = timezone.now()
	return render(request, 'mca_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })


def mca_proj(request, pk):
	leader = MCA.objects.get(id=pk)
	county_leaders = MCA.objects.all()
	today = timezone.now()
	updates = MCAProject.objects.filter(mca=leader)

	return render(request, 'mca_projects.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def mca_ext_proj(request, pk):
	update = MCAProject.objects.get(id=pk)
	other = MCAProject.objects.exclude(id=pk)
	leaders = MCA.objects.all()

	today = timezone.now()
	return render(request, 'mca_proj_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })


def min_updates(request, pk):
	leader = Ministry.objects.get(id=pk)
	county_leaders = Ministry.objects.exclude(id=pk)
	today = timezone.now()
	updates = MinistryUpdates.objects.filter(ministry=leader)

	return render(request, 'min_details.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def min_ext(request, pk):
	update = MinistryUpdates.objects.get(id=pk)
	other = MinistryUpdates.objects.exclude(id=pk)
	leaders = Ministry.objects.all()
	c = Leader.objects.all()

	today = timezone.now()
	return render(request, 'min_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })


def min_proj(request, pk):
	leader = Ministry.objects.get(id=pk)
	county_leaders = Ministry.objects.all()
	today = timezone.now()
	updates = MinistryProject.objects.filter(ministry=leader)

	return render(request, 'min_projects.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def min_ext_proj(request, pk):
	update = MinistryProject.objects.get(id=pk)
	other = MinistryProject.objects.exclude(id=pk)
	leaders = Ministry.objects.all()

	today = timezone.now()
	return render(request, 'min_proj_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })


def uni_updates(request, pk):
	leader = Union.objects.get(id=pk)
	county_leaders = Union.objects.exclude(id=pk)
	today = timezone.now()
	updates = UnionUpdates.objects.filter(union=leader)

	return render(request, 'uni_details.html', {'leader_updates': updates, 'leader': leader,
		'county_leaders': county_leaders, 'today': today, })

def uni_ext(request, pk):
	update = UnionUpdates.objects.get(id=pk)
	other = UnionUpdates.objects.exclude(id=pk)
	leaders = Union.objects.all()

	today = timezone.now()
	return render(request, 'uni_ext.html', {'update': update, 'other': other, 'today': today,
	'county_leaders': leaders, })

def leader_log(request):
	return render(request, 'leader_start.html', {})

def index(request):
	return render(request, 'adminbar.html', {})

def home(request):
	return render(request, 'start.html', {})