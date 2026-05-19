"""模型数据库测试"""

import pytest

from llmpick.models import ModelDatabase
from llmpick.types import QuantizationType


class TestModelDatabase:
    """测试模型数据库"""

    def test_database_initialization(self):
        """测试数据库初始化"""
        db = ModelDatabase()
        assert len(db.models) > 0

    def test_get_all_models(self):
        """测试获取所有模型"""
        db = ModelDatabase()
        models = db.get_all_models()
        assert len(models) > 0
        assert all(hasattr(m, "id") for m in models)

    def test_get_model_by_id(self):
        """测试根据ID获取模型"""
        db = ModelDatabase()
        model = db.get_model_by_id("qwen2.5-7b")
        
        assert model is not None
        assert model.name == "Qwen2.5-7B"
        assert model.is_chinese_optimized

    def test_get_model_by_id_not_found(self):
        """测试获取不存在的模型"""
        db = ModelDatabase()
        model = db.get_model_by_id("non-existent")
        assert model is None

    def test_filter_by_vram(self):
        """测试按显存过滤"""
        db = ModelDatabase()
        models = db.filter_by_vram(8.0)
        
        assert len(models) > 0
        assert all(m.size_gb <= 8.0 * 0.8 for m in models)

    def test_filter_by_tags(self):
        """测试按标签过滤"""
        db = ModelDatabase()
        models = db.filter_by_tags(["qwen"])
        
        assert len(models) > 0
        assert all("qwen" in [t.lower() for t in m.tags] for m in models)

    def test_get_chinese_optimized(self):
        """测试获取中文优化模型"""
        db = ModelDatabase()
        models = db.get_chinese_optimized()
        
        assert len(models) > 0
        assert all(m.is_chinese_optimized for m in models)

    def test_get_code_optimized(self):
        """测试获取代码优化模型"""
        db = ModelDatabase()
        models = db.get_code_optimized()
        
        assert all(m.is_code_optimized for m in models)
