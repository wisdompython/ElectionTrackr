from django.db import models

# Create your models here.

class ElectionCategory(models.Model):
    id = models.IntegerField(primary_key=True,unique=True)
    category_name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.category_name
class Agentname(models.Model):
    name_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=13)
    pollingunit_uniqueid = models.IntegerField()

   


class AnnouncedLgaResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    lga_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)
    voting_category = models.ForeignKey('ElectionCategory', on_delete=models.DO_NOTHING)


    
class AnnouncedPuResults(models.Model):
    result_id = models.AutoField(primary_key=True,unique=True)
    polling_unit_uniqueid = models.ForeignKey('New_Polling_Unit',on_delete=models.DO_NOTHING, related_name='pu_results')
    party_abbreviation = models.ForeignKey("Party", on_delete=models.DO_NOTHING)
    party_score = models.IntegerField(null=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)
    voting_category = models.ForeignKey('ElectionCategory', on_delete=models.DO_NOTHING)

    

    
        
class AnnouncedStateResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)
    voting_category = models.ForeignKey('ElectionCategory', on_delete=models.DO_NOTHING)



class AnnouncedWardResults(models.Model):
    result_id = models.AutoField(primary_key=True)
    ward_name = models.CharField(max_length=50)
    party_abbreviation = models.CharField(max_length=4)
    party_score = models.IntegerField()
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)
    voting_category = models.ForeignKey('ElectionCategory', on_delete=models.DO_NOTHING)

    def __str__(self) -> str:
        return self.ward_name

    

class Lga(models.Model):
    uniqueid = models.AutoField(primary_key=True)
    lga_id = models.IntegerField(unique=True)
    lga_name = models.CharField(max_length=50)
    state_id = models.ForeignKey('States', on_delete=models.DO_NOTHING)
    lga_description = models.TextField(blank=True, null=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.lga_name


class Party(models.Model):
    partyid = models.CharField(max_length=11)
    partyname = models.CharField(max_length=11)

    
    def __str__(self):
        return self.partyname
    
    @property
    def get_total_by_party(self, voting_category):
        self.voting_category=voting_category
        print(voting_category)
        total_party = self.party_total.filter(party=self, voting_category=self.voting_category)
        print(sum([score.party_score for score in total_party]))    
        return sum([score.party_score for score in total_party])


class PollingUnit(models.Model):
    uniqueid = models.AutoField(primary_key=True)
    polling_unit_id = models.IntegerField(unique=True)
    ward_id = models.ForeignKey('Ward', on_delete=models.DO_NOTHING)
    polling_unit_number = models.CharField(max_length=50, blank=True, null=True,unique=True)
    polling_unit_name = models.CharField(max_length=50, blank=True, null=True)
    polling_unit_description = models.TextField(blank=True, null=True)
    lat = models.CharField(max_length=255, blank=True, null=True)
    long = models.CharField(max_length=255, blank=True, null=True)
    entered_by_user = models.CharField(max_length=50, blank=True, null=True)
    date_entered = models.DateTimeField(blank=True, null=True)
    user_ip_address = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.polling_unit_name
    
    

class New_Polling_unit(models.Model):
    polling_unit = models.ForeignKey('PollingUnit', on_delete=models.CASCADE, null=True)
    party = models.ForeignKey('Party',on_delete=models.CASCADE, null=True, related_name='party_total')
    voting_category = models.ForeignKey('ElectionCategory', on_delete=models.DO_NOTHING)
    party_score = models.IntegerField()

    def __str__(self):
        return self.polling_unit.polling_unit_name
    


class States(models.Model):
    state_id = models.IntegerField(primary_key=True,unique=True)
    state_name = models.CharField(max_length=50)

    def __str__(self):
        return self.state_name
    
  


class Ward(models.Model):
    uniqueid = models.AutoField(primary_key=True,unique=True)
    ward_id = models.IntegerField(unique=True)
    ward_name = models.CharField(max_length=50)
    lga_id = models.ForeignKey('Lga', on_delete=models.DO_NOTHING)
    ward_description = models.TextField(blank=True, null=True)
    entered_by_user = models.CharField(max_length=50)
    date_entered = models.DateTimeField()
    user_ip_address = models.CharField(max_length=50)

   

    def __str__(self):
        return self.ward_name