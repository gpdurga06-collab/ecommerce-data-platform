import zipfile

with zipfile.ZipFile('handler.zip', 'w') as z:
    z.write('handler.py')
    print('Done! handler.zip created successfully!')