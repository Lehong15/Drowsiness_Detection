# import the necessary packages
from scipy.spatial import distance as dist

def is_close(eye,threshold):
	# 计算两组垂直眼标之间的距离
	A = dist.euclidean(eye[1], eye[5])
	B = dist.euclidean(eye[2], eye[4])

	# 计算水平眼标间的距离
	C = dist.euclidean(eye[0], eye[3])

	# 计算眼镜纵横比
	ear = (A + B) / (2.0 * C)
	# print(ear)
	if ear < threshold:
		return True


def close_count(eyes, threshold):
	count = 0
	for eye in eyes:
		right = eye[0:6]
		left = eye[6:12]
		
		if is_close(right,threshold) and is_close(left,threshold):
			count += 1
	return count

# #test
# eyes = [[(175, 146), (194, 147), (209, 145), (225, 145), (209, 148), (194, 148), (293, 142), (309, 142), (322, 142), (336, 141), (323, 143), (309, 144)]]
# print(close_count(eyes,0.2))
