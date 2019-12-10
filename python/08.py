#!/usr/bin/python3

with open('../input/08.txt') as f:
    data = f.read()

layers = []
for i in range(0, len(data), 25*6):
    layer_data = data[i:i+(25*6)]
    layer = [int(c) for c in layer_data]
    layers.append(layer)


layer_with_fewest_zeroes = None
fewest_zeroes = len(data)
for layer in layers:
    zeroes = layer.count(0)
    if zeroes < fewest_zeroes:
        fewest_zeroes = zeroes
        layer_with_fewest_zeroes = layer

print(layer_with_fewest_zeroes.count(1) * layer_with_fewest_zeroes.count(2))


final_image = []
for i in range(25*6):
    for layer in layers:
        if layer[i] == 0:
            final_image.append('X')
            break
        elif layer[i] == 1:
            final_image.append(' ')
            break
    else:
        final_image.append(' ')

print(''.join(final_image[0:25]))
print(''.join(final_image[25:50]))
print(''.join(final_image[50:75]))
print(''.join(final_image[75:100]))
print(''.join(final_image[100:125]))
print(''.join(final_image[125:150]))