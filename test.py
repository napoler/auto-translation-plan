
from albert_pytorch import classify
text="""

是一个包 albert_pytorch

# fix 修正提交错误

版本更新日志 0.0.2.1.3 修复了cpu运行时候错误

0.0.1.9 训练加入自动随机屏蔽数据15% 适用于所有数据 0.0.1.7 版本之前的请勿使用 0.0.2.1 加入处理两句话的判断操作 分类示例 from albert_pytorch import classify tclass = classify(model_name_or_path=’outputs/terry_r_rank/’,num_labels=1,device=’cuda’) p=tclass.pre(text)


"""
tclass = classify(model_name_or_path="/mnt/data/dev/model/classification-text-good-bad/model",num_labels=2,device="cpu") 
p=tclass.pre(text)
print(p)
# 