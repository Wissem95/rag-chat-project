import ssl
import nltk

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Télécharger toutes les ressources nécessaires
resources = [
    'punkt',
    'punkt_tab',
    'stopwords',
    'averaged_perceptron_tagger',
    'universal_tagset'
]

for resource in resources:
    try:
        nltk.download(resource)
        print(f"✅ {resource} téléchargé avec succès")
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement de {resource}: {str(e)}")
