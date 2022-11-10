# Script to sort photos in a directory based on whether they have any content

[PROJECT PAGE](https://hawier.dev/scripts/images_segregator.html)

The script allows you to segregate photos in a folder based on whether there is any content in the photo.

As arguments the user gives the path to the directory containing photos and one of the two arguments --black or --white
which means the background color.

Requirements:
```shell
numpy
opencv-python
```

## Examples:

```shell
python images_segregator.py --path images --white
```

example_image_with_no_content.png

![image_no_content](./image_no_content.png)

example_image_with_content.png

![image_with_content](./image_with_content.png)

- Input directory tree
```shell
images
├── segregator_no_content.png
└── segregator_with_content.png
```
- Output directory tree
```shell
images
├── content
│   └── segregator_with_content.png
└── no_content
    └── segregator_no_content.png
```

