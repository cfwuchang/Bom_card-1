
from odoo import api,fields,models,_
import datetime
class BomCard(models.Model):
	_name = 'bom.card'
	_description = '生产npm卡'
	_rec_name = 'name'
	_date_name = 'date'
	_check_companycheck_company=True

	user=fields.Many2one(string=u"名字",comodel_name="res.users",required=True)
	date_from = fields.Date(string=u"开始时间",required=True)
	date_to = fields.Date(string=u"结束时间",required=True)
	name=fields.Char(string=u"标识",required=True)
	comparison=fields.Many2one(string=u"上个月标识",comodel_name='bom.card')
	
# 	money=fields.Monetary(string=u"金额",help='非自动计算值，需要手动填写')
	comparison_data=fields.Html(string=u"对比数据",compute='_get_comparison_data')
	
	project=fields.Html(string=u"bom项目",compute='_get_project')
	project_adds=fields.Html(string=u"制造订单增加项目",compute='_get_project_adds')
	project_amend=fields.Html(string=u"制造订单修改项目",compute='_get_project_amend')


	bom_line_ids=fields.Many2many(comodel_name="mrp.bom.line", string=u"bom总列表", compute='_get_attachment_ids')
	bom_line_num=fields.Integer(string=u"bom总列表个数",compute='_get_attachment_ids_name')

	bom_father=fields.Char(string=u"bom的父级",compute='_get_bom_father')
	bom_father_num=fields.Integer(string=u"bom的父级个数",compute='_get_bom_father_num')


	bom_line_ids_j=fields.Many2many(comodel_name="mrp.bom.line", string=u"bom加工件列表",compute='_get_j')
	bom_line_ids_j_num=fields.Integer(string=u"bom加工件列表个数",compute='_get_j_name')


	bom_line_ids_q=fields.Many2many(comodel_name="mrp.bom.line", string=u"bom选型列表", compute='_get_q')
	bom_line_ids_q_num=fields.Integer(string=u"bom选型列表个数",compute='_get_q_name')


	adds=fields.Many2many(comodel_name="stock.move", string=u"制造订单的列表", compute='_get_move')
	adds_num=fields.Integer(string=u"制造订单的列表个数",compute='_get_move_num')

	father=fields.Char(string=u"制造订单的父级",compute='_get_father')
	father_num=fields.Integer(string=u"制造订单的父级个数",compute='_get_father_num')




	def _get_attachment_ids(self):
		att_model = self.env['mrp.bom.line'] #获取附件模型
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))]   #根据res_model和res_id查询附件
			obj.bom_line_ids = att_model.search(query) #取得附件list
	def _get_attachment_ids_name(self):
		att_model = self.env['mrp.bom.line'] 
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))] 
			obj.bom_line_num = att_model.search(query,count=True)
	
	def _get_j(self):
		att_model = self.env['mrp.bom.line']
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('x_category','=','加工件'),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))] 
			obj.bom_line_ids_j = att_model.search(query) 
	def _get_j_name(self):
		att_model = self.env['mrp.bom.line'] 
		for obj in self:
			query = [('create_uid', '=', obj.user.name), ('x_category','=','加工件'),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))]
			obj.bom_line_ids_j_num = att_model.search(query,count=True)

	def _get_q(self):
		att_model = self.env['mrp.bom.line'] 
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('x_category','!=','加工件'),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))]
			obj.bom_line_ids_q = att_model.search(query)
	def _get_q_name(self):
		att_model = self.env['mrp.bom.line']
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('x_category','!=','加工件'),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))]
			obj.bom_line_ids_q_num = att_model.search(query,count=True)


	def _get_move(self):
		att_model = self.env['stock.move']
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d")),
			("reference","ilike","WH/MO"),('state','!=','confirmed')]
			obj.adds = att_model.search(query)
	def _get_move_num(self):
		att_model = self.env['stock.move'] 
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d")),
			("reference","ilike","WH/MO"),('state','!=','confirmed')]
			obj.adds_num = att_model.search(query,count=True)

	def _get_father(self):
		att_model = self.env['stock.move']
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d")),
			("reference","ilike","WH/MO"),('state','!=','confirmed')]
			# obj.father= att_model.search(query)
			dd=[]
			for i in att_model.search(query):
				aa=i.raw_material_production_id.product_id.name
				dd.append(aa)
			dd=list(set(dd))
			# dd=','.join(dd)
			obj.father=dd

	def _get_father_num(self):
		att_model = self.env['stock.move']
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d")),
			("reference","ilike","WH/MO"),('state','!=','confirmed')]
			# obj.father_num = att_model.search(query,count=True)
			dd=[]
			for i in att_model.search(query):
				aa=i.raw_material_production_id
				dd.append(aa)
			dd=list(set(dd))
			obj.father_num =len(dd)
	

	def _get_bom_father(self):
		att_model = self.env['mrp.bom.line']
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))]
			# obj.bom_father = att_model.search(query)
			dd=[]
			for i in att_model.search(query):
				aa=i.bom_id.display_name
				dd.append(aa)
			dd=list(set(dd))
			dd=','.join(dd)
			obj.bom_father=dd



	def _get_bom_father_num(self):
		att_model = self.env['mrp.bom.line'] 
		for obj in self:
			query = [('create_uid', '=', obj.user.name),('create_date','>=',datetime.datetime.strftime(obj.date_from, "%Y-%m-%d")),
			('create_date','<=',datetime.datetime.strftime(obj.date_to, "%Y-%m-%d"))]
			# obj.bom_father_num = att_model.search(query,count=True)
			dd=[]
			for i in att_model.search(query):
				aa=i.bom_id
				dd.append(aa)
			dd=list(set(dd))
			obj.bom_father_num =len(dd)



	def _get_project(self):
		# bb=list(self.bom_father)

		bb=(self.bom_father).split(',')
		html_str="<table style='width: 70%;text-align: center;'><tr><th>项目</th><th>加工件个数</th><th>选型个数</th></tr>"
		for i in bb:
			dd=0
			ee=0
			html_str += "<tr><td>%s</td>" %(i)
			if self.bom_line_num !=0:
				for j in self.bom_line_ids:
					if j.bom_id.display_name==i:
						if j.x_category!='加工件':
							ee=ee+1
						else:
							dd=dd+1
							
			html_str += "<td>%s</td><td>%s</td>" %(dd,ee)
		html_str += '</table>'
		self.project=html_str


	def _get_project_adds(self):

		bb=(self.father).split(',')
		html_str="<table style='width: 70%;text-align: center;'><tr><th>制造订单新增项目</th><th>新增加工件个数</th><th>新增选型个数</th></tr>"
		for i in bb:
			dd=0
			ee=0
			html_str += "<tr><td>%s</td>" %(i)
			if self.adds_num !=0:
				for j in self.adds:
					if j.x_createUid == False:
						if j.raw_material_production_id.product_id.name==i:
							if j.x_category!='加工件':
								ee=ee+1
							else:
								dd=dd+1
			html_str += "<td>%s</td><td>%s</td>" %(dd,ee)
		html_str += '</table>'
		self.project_adds=html_str
						
		
	def _get_project_amend(self):

		att_model = self.env['stock.move']
		query = [('create_uid', '=', self.user.name),('create_date','>=',datetime.datetime.strftime(self.date_from, "%Y-%m-%d")),
		('create_date','<=',datetime.datetime.strftime(self.date_to, "%Y-%m-%d")),
		("reference","ilike","WH/MO"),('state','!=','confirmed')]

		dd=[]
		for i in att_model.search(query):
			aa=i.raw_material_production_id
			dd.append(aa)
		dd=list(set(dd))



		bb=(self.father).split(',')
		html_str="<table style='width: 70%;text-align: center;'><tr><th>制造订单修改项目</th><th>修改加工件个数</th><th>修改选型个数</th></tr>"
		for i in dd:
			dd=0
			ee=0
			html_str += "<tr><td>%s</td>" %(i.product_id.name)
			if self.adds_num !=0:
				for j in self.adds:
					if j.raw_material_production_id.product_id.name==i.product_id.name:
						if j.x_createUid != False:
							# if j.write_date != i.create_date:
							if datetime.datetime.strftime(j.write_date, "%Y-%m-%d") != datetime.datetime.strftime(i.create_date, "%Y-%m-%d"):
								if j.x_category!='加工件':
									ee=ee+1
								else:
									dd=dd+1
			html_str += "<td>%s</td><td>%s</td>" %(dd,ee)
		html_str += '</table>'
		self.project_amend=html_str


	def _get_comparison_data(self):
		if  self.comparison.user==self.user:
			html_str="<table style='width: 100%;text-align: center;'><tr><th>bom总列表增减数</th><th>bom加工件列表增减数</th><th>bom选型列表增减数</th><th>制造订单的列表增减数</th></tr>"
			aa= self.bom_line_num - self.comparison.bom_line_num
			bb= self.bom_line_ids_j_num - self.comparison.bom_line_ids_j_num
			cc= self.bom_line_ids_q_num - self.comparison.bom_line_ids_q_num
			dd= self.adds_num - self.comparison.adds_num
			html_str += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr></table>" %(aa,bb,cc,dd)
			self.comparison_data=html_str
		else:
			self.comparison_data="<p>对比失败，相同的名字才可以比对</p>"

	
	@api.model
	def create(self, vals):
		if vals.get('name', _('New')) == _('New'):
			vals['name'] = self.env['ir.sequence'].next_by_code('vehicle.delivery.transfer')
		return super(BomCard, self).create(vals)


		
