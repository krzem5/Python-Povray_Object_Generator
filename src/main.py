import panda3d.core
import os



def create(fp,x,y,z,a,b,c):
	fp=os.path.abspath(fp).replace("\\","/")
	vl=[]
	nl=[]
	fl=[]
	txl=[]
	txnml=[]
	c_tx=None
	with open(fp,"rb") as f:
		for k in f.read().replace(b"\r\n",b"\n").split(b"\n"):
			k=k.strip().split(b" ")
			if (k[0] in [b"",b"s",b"o",b"g",b"#",b"vt"]):
				continue
			if (k[0]==b"mtllib"):
				with open(fp[:-len(fp.split("/")[-1])]+str(b" ".join(k[1:]),"utf-8"),"rb") as mf:
					mc_tx=None
					for mk in mf.read().replace(b"\r\n",b"\n").split(b"\n"):
						mk=mk.strip().split(b" ")
						if (mk[0] in [b"",b"#",b"illum",b"Ni",b"Ke",b"Ks",b"Ka",b"Ns",b"d"]):
							continue
						if (mk[0]==b"newmtl"):
							txnml+=[b" ".join(mk[1:])]
						elif (mk[0]==b"Kd"):
							txl+=[(float(mk[1]),float(mk[2]),float(mk[3]))]
			elif (k[0]==b"v"):
				vl+=[(float(k[1]),float(k[2]),float(k[3]))]
			elif (k[0]==b"vn"):
				nl+=[(float(k[1]),float(k[2]),float(k[3]))]
			elif (k[0]==b"f"):
				fl+=[(c_tx,[(int(k[i].split(b"/")[0])-1,int(k[i].split(b"/")[2])-1) for i in range(1,len(k))])]
			elif (k[0]==b"usemtl"):
				c_tx=b" ".join(k[1:])
			else:
				raise RuntimeError(str(k))
	il=[]
	nil=[]
	vhl=[]
	gvl=[]
	for k in fl:
		tl=[k]
		if (len(k[1])>3):
			tc=panda3d.core.Triangulator3()
			tl.clear()
			kl=[]
			for i in range(0,len(k[1])):
				kl+=[k[1][i]]
				tc.addPolygonVertex(tc.addVertex(*vl[k[1][i][0]]))
			tc.triangulate()
			for n in range(0,tc.getNumTriangles()):
				tl+=[(k[0],(kl[tc.getTriangleV0(n)],kl[tc.getTriangleV1(n)],kl[tc.getTriangleV2(n)]))]
		for k in tl:
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
	return f"mesh2 {{\n\tvertex_vectors {{\n\t\t{len(gvl)},\n\t\t{','.join(['<'+str(e[0])+','+str(e[1])+','+str(e[2])+'>' for e in gvl])}\n\t}}\n\tnormal_vectors {{\n\t\t{len(gvl)},\n\t\t{','.join(['<'+str(e[3])+','+str(e[4])+','+str(e[5])+'>' for e in gvl])}\n\t}}\n\ttexture_list{{\n\t\t{len(txl)},\n\t\t{tx2.join([tx0+str(e[0])+','+str(e[1])+','+str(e[2])+tx1 for e in txl])}\n\t}}\n\tface_indices {{\n\t\t{len(il)},\n\t\t{','.join(['<'+str(e[0])+','+str(e[1])+','+str(e[2])+'>,'+str(e[3]) for e in il])}\n\t}}\n\trotate<{a},{b},{c}>\n\ttranslate<{x},{y},{z}>\n}}"



print("""#version 3.6



global_settings {
	assumed_gamma 1.0
}
camera {
	location <0,5,25>
	right x*image_width/image_height
	angle 90
	look_at <0,0,0>
}
plane {
	z,-1000
	pigment {
		rgb<0.498039,0.784313,1>
	}
}
light_source {
	<0,0,-10> rgb<1,1,1>
}
light_source {
	<10,50,30> rgb<0.960784,0.941176,0.607843>
	fade_distance 100
	fade_power 1
	spotlight
}
fog {
	rgb<0.95,0.95,0.95> distance 10000
}""")
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Cloud2.obj",20,10,-10,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Cloud1.obj",-10.5,6.5,-20,0,180,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Pipe.obj",0,0,0,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopRight.obj",4,-1,0,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopMiddle.obj",2,-1,0,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopMiddle.obj",0,-1,0,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_TopLeft.obj",-2,-1,0,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_CenterLeft.obj",-2,-3,0,0,0,0))
print(create("D:/K/Assets/quaterius/out/Platformer Pack/Platformer Pack - Nov 2018/OBJ/Platform_BottomLeft.obj",-2,-5,0,0,0,0))
