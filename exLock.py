# -*- coding: utf-8 -*-
# �r�����b�N�N���X
#
# exLock.py Version 1.01 written by fuku@rouge.gr.jp

#"""�g����
#import exLock
#
#lock = exLock.exLock("./lockPath.LCK")
#lock.lock()
#lock.unlock()
#"""

import os,time,stat

class exLock:

	def __init__(self, lockDir):
		self.lockDir = lockDir
		self.result = False

	def lock(self):
		# 3���ȏ�O�ɍ쐬���ꂽ���b�N�t�@�C�����폜����
		# �����炩�̌����Ŏc�����܂܂ɂȂ������b�N�t�@�C��
		#
		try:
			fileStat = os.stat(self.lockDir)
			timeStamp = fileStat[stat.ST_MTIME]
			if timeStamp < (time.time() - 180): os.rmdir(self.lockDir)
		except:
			pass

		# ���b�N�t�@�C�����쐬���Ă݂�
		# ��5�����ă_���Ȃ玸�s�Ƃ���
		self.result = False
		for i in range(5):
			try:
				os.mkdir(self.lockDir)
				self.result = True	# ���b�N�������ō�����Ƃ�����
				break
			except OSError:
				time.sleep(1)
		return self.result

	def unlock(self):
		if self.result == True:		# �����ō�������b�N�t�@�C���Ȃ����
			os.rmdir(self.lockDir)
		self.result = False

	def __del__(self):
		if self.result == True:		# �����ō�������b�N�t�@�C���Ȃ����
			os.rmdir(self.lockDir)
		self.result = False

