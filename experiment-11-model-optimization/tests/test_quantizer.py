"""
Quantization Engine Unit Tests
Experiment 11 — Model Optimization Experiment (MR23-1CS0436)
"""

import os
from app.services.quantizer import RealQuantizationEngineService

def test_quantization_profiles_and_artifacts():
    quantizer = RealQuantizationEngineService()
    fp32 = quantizer.get_fp32_profile()
    int8 = quantizer.get_int8_profile()
    int4 = quantizer.get_int4_profile()

    assert os.path.exists(fp32.artifact_path)
    assert os.path.exists(int8.artifact_path)
    assert os.path.exists(int4.artifact_path)

    assert int8.level_name == "Symmetric INT8 Weight Quantization"
    assert int8.metrics.serialized_file_size_mb < fp32.metrics.serialized_file_size_mb
    assert int4.metrics.serialized_file_size_mb < int8.metrics.serialized_file_size_mb
    assert int8.metrics.compression_ratio_percent > 0.0
    assert int4.metrics.compression_ratio_percent > int8.metrics.compression_ratio_percent
    assert int8.metrics.measured_latency_ms > 0.0
    assert int8.metrics.synthetic_operations_sec > 0.0
    assert int8.metrics.forward_passes_sec == 0.0

def test_int8_dequantization_round_trip():
    quantizer = RealQuantizationEngineService()
    deq_int8 = quantizer.dequantize_int8()
    assert len(deq_int8) == len(quantizer.fp32_weights)
    mse = quantizer.compute_reconstruction_mse(deq_int8)
    assert mse >= 0.0
    assert mse < 0.05, f"INT8 reconstruction error too high: {mse}"

def test_packed_int4_round_trip_unpacking():
    quantizer = RealQuantizationEngineService()
    deq_int4 = quantizer.unpack_and_dequantize_int4()
    assert len(deq_int4) == len(quantizer.fp32_weights)
    mse = quantizer.compute_reconstruction_mse(deq_int4)
    assert mse >= 0.0
    assert mse < 0.2, f"INT4 reconstruction error too high: {mse}"
