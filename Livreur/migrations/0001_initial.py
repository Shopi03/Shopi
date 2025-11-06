from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Livreur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(help_text='Nom de famille du livreur.', max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(help_text='Prénom du livreur.', max_length=100, verbose_name='Prénom')),
                ('identifiant', models.CharField(help_text="Identifiant unique utilisé pour l'identifié.", max_length=50, unique=True, verbose_name='Identifiant')),
                ('mail', models.EmailField(help_text='Adresse mail utilisée pour la connexion et la communication.', max_length=254, unique=True, verbose_name='Adresse e-mail')),
                ('telephone', models.CharField(help_text='Numéro de Téléphone du livreur.', max_length=15, unique=True, verbose_name='Téléphone')),
                ('profil', models.ImageField(blank=True, help_text='Image représentant le livreur (facultative).', null=True, upload_to='profils_livreur/', verbose_name='Photo de profil')),
                ('genre', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], help_text='Sexe du livreur : M ou F.', max_length=1, verbose_name='Genre')),
                ('date_naissance', models.DateField(help_text='Date de naissance du livreur.', verbose_name='Date de naissance')),
                ('date_embauche', models.DateField(verbose_name="Date de l'embauche")),
                ('actif', models.BooleanField(default=False, verbose_name='Statut de livreur')),
                ('vehicule', models.CharField(max_length=100, verbose_name='Voiture utilisé par le Livreur')),
                ('zone_livraison', models.CharField(max_length=100, verbose_name='Zone de livration')),
                ('mot_de_passe', models.CharField(help_text="Mot de passe chiffré pour l'accès au compte.", max_length=255, verbose_name='Mot de passe')),
                ('date_creation', models.DateTimeField(auto_now_add=True, verbose_name='Date de création du compte')),
            ],
            options={
                'verbose_name': 'livreur',
                'verbose_name_plural': 'livreurs',
                'ordering': ['-date_creation'],
            },
        ),
    ]
