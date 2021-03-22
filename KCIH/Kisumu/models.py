from django.db import models
from passlib.hash import pbkdf2_sha256

class Constituency(models.Model):
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Ward(models.Model):
	constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)

	def __str__(self):
		return self.name

class Position(models.Model):
	position = models.CharField(max_length=255)

	def __str__(self):
		return self.position
		

class Leader(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	image = models.FileField(upload_to='leaders')
	idNo = models.IntegerField()
	is_leader = models.BooleanField(default=True)
	password = models.CharField(max_length=255)
	position = models.ForeignKey(Position, on_delete=models.CASCADE)

	def __str__(self):
		return self.lname

	def verify_password(self, rawpassword):
		return pbkdf2_sha256.verify(rawpassword, self.password)

class MP(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	image = models.FileField(upload_to='mps')
	idNo = models.IntegerField()
	is_mp = models.BooleanField(default=True)
	password = models.CharField(max_length=255)
	constituency = models.ForeignKey(Constituency, on_delete=models.CASCADE)

	def __str__(self):
		return self.lname

	def verify_password(self, rawpassword):
		return pbkdf2_sha256.verify(rawpassword, self.password)

class MCA(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	image = models.FileField(upload_to='mcas')
	idNo = models.IntegerField()
	is_mca = models.BooleanField(default=True)
	password = models.CharField(max_length=255)
	ward = models.ForeignKey(Ward, on_delete=models.CASCADE)

	def __str__(self):
		return self.lname

	def verify_password(self, rawpassword):
		return pbkdf2_sha256.verify(rawpassword, self.password)


class Ministry(models.Model):
	name = models.CharField(max_length=255)
	image = models.FileField(upload_to='ministry_image')
	address = models.CharField(max_length=255)

	def __str__(self):
		return self.name
	
class Union(models.Model):
	name = models.CharField(max_length=255)
	image = models.FileField(upload_to='union_image')

	def __str__(self):
		return self.name



class LeaderProject(models.Model):
	leader = models.ForeignKey(Leader, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='leader_projects')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	description = models.TextField()
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.title

class MPProject(models.Model):
	mp = models.ForeignKey(MP, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='mp_projects')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	description = models.TextField()
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.title

class MCAProject(models.Model):
	mca = models.ForeignKey(MCA, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='mca_projects')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	description = models.TextField()
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.title		

class MinistryProject(models.Model):
	ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='ministry_projects')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	description = models.TextField()
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.title


class LeaderUpdates(models.Model):
	leader = models.ForeignKey(Leader, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='leader_updates')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	message = models.TextField()
		
	def __str__(self):
		return self.title


class MPUpdates(models.Model):
	mp = models.ForeignKey(MP, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='mp_updates')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	message = models.TextField()
		
	def __str__(self):
		return self.title


class MCAUpdates(models.Model):
	mca = models.ForeignKey(MCA, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='mca_updates')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	message = models.TextField()
		
	def __str__(self):
		return self.title


class MinistryUpdates(models.Model):
	ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='ministry_updates')
	location = models.CharField(max_length=255)
	day =models.DateTimeField(auto_now_add=True)
	message = models.TextField()
		
	def __str__(self):
		return self.title


class UnionUpdates(models.Model):
	union = models.ForeignKey(Union, on_delete=models.CASCADE)
	title = models.CharField(max_length=255)
	image = models.FileField(upload_to='union_updates')
	location = models.CharField(max_length=255)
	day = models.DateTimeField(auto_now_add=True)
	message = models.TextField()
		
	def __str__(self):
		return self.title


class Admin(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	idNo = models.IntegerField()
	password = models.CharField(max_length=255)

	def __str__(self):
		return self.lname

	def verify_password(self, rawpassword):
		return pbkdf2_sha256.verify(rawpassword, self.password)


class MinistryOfficial(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	idNo = models.IntegerField()
	is_ministry_off = models.BooleanField(default=True)
	password = models.CharField(max_length=255)
	ministry = models.ForeignKey(Ministry, on_delete=models.CASCADE)

	def __str__(self):
		return self.lname

	def verify_password(self, rawpassword):
		return pbkdf2_sha256.verify(rawpassword, self.password)
		
		
class UnionOfficial(models.Model):
	fname = models.CharField(max_length=255)
	lname = models.CharField(max_length=255)
	idNo = models.IntegerField()
	is_union_off = models.BooleanField(default=True)
	password = models.CharField(max_length=255)
	union = models.ForeignKey(Union, on_delete=models.CASCADE)

	def __str__(self):
		return self.lname

	def verify_password(self, rawpassword):
		return pbkdf2_sha256.verify(rawpassword, self.password)
		

class MPUpdArchive(models.Model):
	sponsor = models.CharField(max_length=255)
	time_archived = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	message = models.TextField()
	day = models.DateTimeField()

	def __str__(self):
		return self.title

class MPProjArchive(models.Model):
	title = models.CharField(max_length=255)
	time_archived = models.DateTimeField(auto_now_add=True)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	location = models.CharField(max_length=255)
	status = models.BooleanField()

	def __str__(self):
		return self.title

class LeaderUpdArchive(models.Model):
	sponsor = models.CharField(max_length=255)
	time_archived = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	message = models.TextField()
	day = models.DateTimeField()

	def __str__(self):
		return self.title

class LeaderProjArchive(models.Model):
	sponsor = models.CharField(max_length=255)
	time_archived = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	location = models.CharField(max_length=255)
	status = models.BooleanField()

	def __str__(self):
		return self.title

class MCAUpdArchive(models.Model):
	sponsor = models.CharField(max_length=255)
	time_archived = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	message = models.TextField()
	day = models.DateTimeField()

	def __str__(self):
		return self.title

class MCAProjArchive(models.Model):
	sponsor = models.CharField(max_length=255)
	time_archived = models.DateTimeField(auto_now_add=True)
	title = models.CharField(max_length=255)
	estimate = models.IntegerField()
	allocation = models.IntegerField()
	location = models.CharField(max_length=255)
	status = models.BooleanField()

	def __str__(self):
		return self.title


		
		