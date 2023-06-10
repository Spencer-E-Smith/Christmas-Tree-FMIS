import matplotlib.pyplot as plt
import matplotlib.image as mpimg

fig, ax = plt.subplots()

atlas_data = [['Shack top right',
  38.7388513104658,
  -120.716202587551
],
 ['house entrance',
  38.74106174194,
  -120.714668543139
]
,
 ['end of fence',
  38.73902051174787,
  -120.71743439598214
]
,
 ['road block',
  38.74108972167316,
  -120.71689001695219
]
,
 ['tree by road',
  38.7412377357718,
  -120.71524649341036
]
]

def mapping_data(atlas_data):
    x, y = [], []
    for i in range(len(atlas_data)):
        x.append(atlas_data[i][1])
        y.append(atlas_data[i][2])

    return x, y

y, x = mapping_data(atlas_data)

ax.scatter(x, y, edgecolors='red', linewidths=1, zorder=2)
ax.imshow(mpimg.imread('C:\\Users\\python_account\\Pictures\\farm north.JPG'), extent=(-120.717566420228, -120.71407, 38.7385559849825, 38.74139), zorder=1)

plt.show()