import panda3d.core
import os



def load(fp,x,y,z):
	def _flt(v):
		return ("%.4f"%v).rstrip("0").rstrip(".")
	vl=[]
	nl=[]
	fl=[]
	txl=[]
	txnml=[]
	fp=os.path.abspath(fp).replace("\\","/")
	c_tx=None
	with open(fp,"rb") as f:
		for k in f.read().replace(b"\r\n",b"\n").split(b"\n"):
			k=k.strip().split(b" ")
			if (k[0] in [b"",b"s",b"o",b"g",b"#",b"vt"]):
				continue
			if (k[0]==b"mtllib"):
				with open(fp[:-len(fp.split("/")[-1])]+str(b" ".join(k[1:]),"utf-8"),"rb") as mf:
					mc_tx=False
					for mk in mf.read().replace(b"\r\n",b"\n").split(b"\n"):
						mk=mk.strip().split(b" ")
						if (mk[0] in [b"",b"#",b"illum",b"Ni",b"Ke",b"Ks",b"Ka",b"Ns",b"d"]):
							continue
						if (mk[0]==b"newmtl"):
							if (b" ".join(mk[1:]) not in txnml):
								txnml+=[b" ".join(mk[1:])]
								mc_tx=True
							else:
								mc_tx=False
						elif (mk[0]==b"Kd" and mc_tx):
							txl+=[(float(mk[1]),float(mk[2]),float(mk[3]))]
			elif (k[0]==b"v"):
				vl+=[(float(k[1])+x,float(k[2])+y,float(k[3])+z)]
			elif (k[0]==b"vn"):
				nl+=[(float(k[1]),float(k[2]),float(k[3]))]
			elif (k[0]==b"f"):
				if (len(k)-1>3):
					tc=panda3d.core.Triangulator3()
					kl=[]
					k=[(int(k[i].split(b"/")[0])-1,int(k[i].split(b"/")[2])-1) for i in range(1,len(k))]
					for i in range(0,len(k)):
						kl+=[k[i]]
						tc.addPolygonVertex(tc.addVertex(*vl[k[i][0]]))
					tc.triangulate()
					for n in range(0,tc.getNumTriangles()):
						fl+=[(c_tx,(kl[tc.getTriangleV0(n)],kl[tc.getTriangleV1(n)],kl[tc.getTriangleV2(n)]))]
				else:
					fl+=[(c_tx,[(int(k[i].split(b"/")[0])-1,int(k[i].split(b"/")[2])-1) for i in range(1,len(k))])]
			elif (k[0]==b"usemtl"):
				c_tx=b" ".join(k[1:])
			else:
				raise RuntimeError(str(k))
	for i,k in enumerate(vl):
		vl[i]=(_flt(k[0]),_flt(k[1]),_flt(k[2]))
	return (vl,nl,fl,txnml,txl)



def move(e,dx,dy,dz,fc):
	def _flt(v):
		return ("%.4f"%v).rstrip("0").rstrip(".")
	vl=e[0]
	for i,k in enumerate(vl):
		vl[i]=((f"{k[0]}+clock*{_flt(dx/fc)}" if dx!=0 else k[0]),(f"{k[1]}+clock*{_flt(dy/fc)}" if dy!=0 else k[1]),(f"{k[2]}+clock*{_flt(dz/fc)}" if dz!=0 else k[2]))
	return (vl,*e[1:])



def write(*dt):
	def _flt(v):
		return ("%.4f"%v).rstrip("0").rstrip(".")
	il=[]
	vhl=[]
	gvl=[]
	txl=[]
	txnml=[]
	for (vl,nl,fl,txnml2,txl2) in dt:
		for i,k in enumerate(txnml2):
			if (k not in txnml):
				txnml+=[k]
				txl+=[txl2[i]]
		for k in fl:
			o=[]
			for i in range(0,3):
				v=(*vl[k[1][i][0]],*nl[k[1][i][1]])
				h=hash(v)
				if (h not in vhl):
					o+=[len(vhl)]
					vhl+=[h]
					gvl+=[v]
				else:
					o+=[vhl.index(h)]
			o+=[txnml.index(k[0])]
			il+=[o]
	tx0="texture {\n\t\t\tpigment {\n\t\t\t\trgb<"
	tx1=">\n\t\t\t}\n\t\t}"
	tx2=",\n\t\t"
	return f"mesh2 {{\n\tvertex_vectors {{\n\t\t{len(gvl)},\n\t\t{','.join(['<'+e[0]+','+e[1]+','+e[2]+'>' for e in gvl])}\n\t}}\n\tnormal_vectors {{\n\t\t{len(gvl)},\n\t\t{','.join(['<'+_flt(e[3])+','+_flt(e[4])+','+_flt(e[5])+'>' for e in gvl])}\n\t}}\n\ttexture_list{{\n\t\t{len(txl)},\n\t\t{tx2.join([tx0+_flt(e[0])+','+_flt(e[1])+','+_flt(e[2])+tx1 for e in txl])}\n\t}}\n\tface_indices {{\n\t\t{len(il)},\n\t\t{','.join(['<'+_flt(e[0])+','+_flt(e[1])+','+_flt(e[2])+'>,'+_flt(e[3]) for e in il])}\n\t}}\n}}"



print("#version 3.6\n\n\n\nglobal_settings {\n\tassumed_gamma 1.0\n}\ncamera {\n\tlocation <2,5,25>\n\tright x*image_width/image_height\n\tangle 90\n\tlook_at <2,0,0>\n}\nplane {\n\tz,-1000\n\tpigment {\n\t\trgb<0.498039,0.784313,1>\n\t}\n}\nlight_source {\n\t<0,0,-10> rgb<1,1,1>\n}\nlight_source {\n\t<7.5,60,35> rgb<0.960784,0.941176,0.607843>*1.5\n\tfade_distance 150\n\tfade_power 1.5\n\tspotlight\n}\nfog {\n\trgb<0.95,0.95,0.95> distance 5000\n}")
print(write(
	move(load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Cloud2.obj",20,10,-10),-40,0,0,120),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Cloud1.obj",-6.5,6.5,-10),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopRight.obj",4,-1,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopMiddle.obj",2,-1,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopMiddle.obj",0,-1,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopLeft.obj",-2,-1,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_CenterRight.obj",4,-3,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_CenterMiddle.obj",2,-3,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_CenterMiddle.obj",0,-3,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_CenterLeft.obj",-2,-3,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomRight.obj",4,-5,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomMiddle.obj",2,-5,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomMiddle.obj",0,-5,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomLeft.obj",-2,-5,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Pipe.obj",0,0,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Grass.obj",-2,0,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Rock2.obj",4,0,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopRight.obj",-8,2,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopLeft.obj",-10,2,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomRight.obj",-8,0,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomLeft.obj",-10,0,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Sign_Right.obj",-8,3,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Tree2.obj",-10,2,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/MovingPlatform_Long.obj",15,-5,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Ladder_long.obj",13,-4.3,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Spikes_Platform.obj",15,-4.5,0),
	load("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Lever.obj",17,-4,0),
))
