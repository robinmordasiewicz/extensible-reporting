ARG FUNCTION_DIR="/function"

FROM public.ecr.aws/docker/library/python:bookworm as build-image

ARG FUNCTION_DIR="/function"

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY lambda_requirements.txt ${FUNCTION_DIR}
# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric
RUN pip install \
    --target ${FUNCTION_DIR} \
        -r ${FUNCTION_DIR}/lambda_requirements.txt


FROM public.ecr.aws/docker/library/python:bookworm
ARG FUNCTION_DIR
RUN apt-get update && \
    apt-get install -y xfonts-75dpi xfonts-base
RUN apt-get install -y curl && \
 curl -LJO https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_amd64.deb \
 && dpkg -i wkhtmltox_0.12.6.1-3.bookworm_amd64.deb



# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
COPY lambda_function.py ${FUNCTION_DIR}
COPY assets ${FUNCTION_DIR}/assets
COPY modules ${FUNCTION_DIR}/modules
COPY templates ${FUNCTION_DIR}/templates
ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["lambda_function.lambda_handler"]



