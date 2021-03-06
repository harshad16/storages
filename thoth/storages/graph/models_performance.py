#!/usr/bin/env python3
# thoth-storages
# Copyright(C) 2019 Fridolin Pokorny
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Performance indicators (models) used in Thoth with their schemas."""

from functools import partial
import logging

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy import Float
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session

from .models_base import BaseExtension
from .models_base import Base

_LOGGER = logging.getLogger(__name__)


class PerformanceIndicatorBase:
    """A base class for implementing performance indicators."""

    # ML framework used for the performance indicator.
    framework = Column(String(256), nullable=True)

    # Origin from where the performance indicator was obtained. In case of Git repo,
    # it holds Git repo URL, in case of URL it holds URL to the script.
    origin = Column(String(256), nullable=True)

    # Reference of the script, in case of Git repo it holds commit SHA, in case of URL it carries
    # SHA256 of the script which was used to test the performance with (performance indicator script).
    version = Column(String(256), nullable=False)

    # This one is used later on in queries in adviser, all the relevant performance indicators should
    # respect this property and place results in there.
    overall_score = Column(Float, nullable=True)

    # The actual exit code of the performance indicator.
    exit_code = Column(Integer, nullable=False)

    # Process statistics:
    #   https://docs.python.org/3/library/resource.html#resource.getrusage
    ru_utime = Column(Float, nullable=False)
    ru_stime = Column(Float, nullable=False)
    ru_maxrss = Column(Integer, nullable=False)
    ru_ixrss = Column(Integer, nullable=False)
    ru_idrss = Column(Integer, nullable=False)
    ru_isrss = Column(Integer, nullable=False)
    ru_minflt = Column(Integer, nullable=False)
    ru_majflt = Column(Integer, nullable=False)
    ru_nswap = Column(Integer, nullable=False)
    ru_inblock = Column(Integer, nullable=False)
    ru_oublock = Column(Integer, nullable=False)
    ru_msgsnd = Column(Integer, nullable=False)
    ru_msgrcv = Column(Integer, nullable=False)
    ru_nsignals = Column(Integer, nullable=False)
    ru_nvcsw = Column(Integer, nullable=False)
    ru_nivcsw = Column(Integer, nullable=False)

    @classmethod
    def create_from_report(
        cls, session: Session, inspection_document: dict, inspection_run_id: int
    ) -> "PerformanceIndicatorBase":
        """Create performance indicator record together with related observed performance edge based on inspection."""
        # Place core parts of the base class into the model.
        framework = inspection_document["job_log"]["stdout"].get("framework")
        if not framework:
            _LOGGER.warning("No machine learning framework specified in performance indicator %r", cls.__name__)

        overall_score = inspection_document["job_log"]["stdout"].get("overall_score")
        if overall_score is None:
            _LOGGER.warning("No overall score detected in performance indicator %r", overall_score)

        partial_model = partial(
            cls.get_or_create,
            session,
            inspection_run_id=inspection_run_id,
            framework=framework,
            origin=inspection_document["specification"]["script"],
            version=inspection_document["job_log"]["stdout"].get("version")
            or inspection_document["job_log"]["script_sha256"],
            overall_score=overall_score,
            exit_code=inspection_document["job_log"].get("exit_code"),
            ru_utime=inspection_document["job_log"].get("usage", {}).get("ru_utime"),
            ru_stime=inspection_document["job_log"].get("usage", {}).get("ru_stime"),
            ru_maxrss=inspection_document["job_log"].get("usage", {}).get("ru_maxrss"),
            ru_ixrss=inspection_document["job_log"].get("usage", {}).get("ru_ixrss"),
            ru_idrss=inspection_document["job_log"].get("usage", {}).get("ru_idrss"),
            ru_isrss=inspection_document["job_log"].get("usage", {}).get("ru_isrss"),
            ru_minflt=inspection_document["job_log"].get("usage", {}).get("ru_minflt"),
            ru_majflt=inspection_document["job_log"].get("usage", {}).get("ru_majflt"),
            ru_nswap=inspection_document["job_log"].get("usage", {}).get("ru_nswap"),
            ru_inblock=inspection_document["job_log"].get("usage", {}).get("ru_inblock"),
            ru_oublock=inspection_document["job_log"].get("usage", {}).get("ru_oublock"),
            ru_msgsnd=inspection_document["job_log"].get("usage", {}).get("ru_msgsnd"),
            ru_msgrcv=inspection_document["job_log"].get("usage", {}).get("ru_msgrcv"),
            ru_nsignals=inspection_document["job_log"].get("usage", {}).get("ru_nsignals"),
            ru_nvcsw=inspection_document["job_log"].get("usage", {}).get("ru_nvcsw"),
            ru_nivcsw=inspection_document["job_log"].get("usage", {}).get("ru_nivcsw"),
        )

        return cls.from_report(inspection_document, partial_model)

    @classmethod
    def from_report(cls, inspection_document: dict, partial_model: type(partial)) -> "PerformanceIndicatorBase":
        """Create model from the inspection report respecting parameters and result reported by the indicator."""
        kwargs = {}
        for parameter, parameter_value in inspection_document["job_log"]["stdout"]["@parameters"].items():
            kwargs[parameter] = parameter_value

        for result_name, result_value in inspection_document["job_log"]["stdout"]["@result"].items():
            if result_name in kwargs:
                raise ValueError("Collision in result name and parameter name")

            kwargs[result_name] = result_value

        return partial_model(**kwargs)


class PiMatmul(Base, BaseExtension, PerformanceIndicatorBase):
    """A class for representing a matrix multiplication micro-performance test."""

    __tablename__ = "pi_matmul"

    id = Column(Integer, primary_key=True, autoincrement=True)

    inspection_run_id = Column(Integer, ForeignKey("inspection_run.id"), nullable=False)
    inspection_run = relationship("InspectionRun", back_populates="matmul_perf_indicators")

    # Device used during performance indicator run - CPU/GPU/TPU/...
    device = Column(String(256), nullable=False)

    # Size of the matrix tested.
    matrix_size = Column(Integer, nullable=False)

    # Type of item in the matrix.
    dtype = Column(String(256), nullable=False)

    # Number of repetitions of matrix multiplication performed.
    reps = Column(Integer, nullable=False)

    # Elapsed seconds.
    elapsed = Column(Float, nullable=False)

    # Final rate gflops/s.
    rate = Column(Float, nullable=False)


class PiConv1D(Base, BaseExtension, PerformanceIndicatorBase):
    """A class for representing a conv1D micro-performance test."""

    __tablename__ = "pi_conv1d"

    id = Column(Integer, primary_key=True, autoincrement=True)

    inspection_run_id = Column(Integer, ForeignKey("inspection_run.id"), nullable=False)
    inspection_run = relationship("InspectionRun", back_populates="conv1d_perf_indicators")

    # Device used during performance indicator run - CPU/GPU/TPU/...
    device = Column(String(256), nullable=False)

    # Type of item in the tensor.
    dtype = Column(String(256), nullable=False)

    # Number of repetitions of conv2d performed.
    reps = Column(Integer, nullable=False)

    # Data format NHWC Channel_last or NCHW Channel_first
    data_format = Column(String(256), nullable=False)

    # INPUT TENSOR
    batch = Column(Integer, nullable=False)
    input_width = Column(Integer, nullable=False)
    input_channels = Column(Integer, nullable=False)

    # FILTER
    filter_width = Column(Integer, nullable=False)
    output_channels = Column(Integer, nullable=False)

    # Stride, the speed by which the filter moves across the image
    strides = Column(Integer, nullable=False)

    # Padding
    padding = Column(String(256), nullable=False)

    # Elapsed seconds.
    elapsed = Column(Float, nullable=False)

    # Final rate gflops/s.
    rate = Column(Float, nullable=False)


class PiConv2D(Base, BaseExtension, PerformanceIndicatorBase):
    """A class for representing a conv2D micro-performance test."""

    __tablename__ = "pi_conv2d"

    id = Column(Integer, primary_key=True, autoincrement=True)

    inspection_run_id = Column(Integer, ForeignKey("inspection_run.id"), nullable=False)
    inspection_run = relationship("InspectionRun", back_populates="conv2d_perf_indicators")

    # Device used during performance indicator run - CPU/GPU/TPU/...
    device = Column(String(256), nullable=False)

    # Type of item in the tensor.
    dtype = Column(String(256), nullable=False)

    # Number of repetitions of conv2d performed.
    reps = Column(Integer, nullable=False)

    # Data format NHWC Channel_last or NCHW Channel_first
    data_format = Column(String(256), nullable=False)

    # INPUT TENSOR
    batch = Column(Integer, nullable=False)
    input_height = Column(Integer, nullable=False)
    input_width = Column(Integer, nullable=False)
    input_channels = Column(Integer, nullable=False)

    # FILTER
    filter_height = Column(Integer, nullable=False)
    filter_width = Column(Integer, nullable=False)
    output_channels = Column(Integer, nullable=False)

    # Stride, the speed by which the filter moves across the image
    strides = Column(Integer, nullable=False)

    # Padding
    padding = Column(String(256), nullable=False)

    # Elapsed seconds.
    elapsed = Column(Float, nullable=False)

    # Final rate gflops/s.
    rate = Column(Float, nullable=False)


# ALL_PERFORMANCE_MODELS = frozenset((ObservedPerformance, PiMatmul, PiConv1D, PiConv2D))
ALL_PERFORMANCE_MODELS = frozenset((PiMatmul, PiConv1D, PiConv2D))


PERFORMANCE_MODEL_BY_NAME = {model_class.__name__: model_class for model_class in ALL_PERFORMANCE_MODELS}
