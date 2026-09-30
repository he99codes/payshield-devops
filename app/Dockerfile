# ==============================================================================
# PayShield FinTech Payment Gateway - Production Dockerfile
# Maintainer: he99codes
# Compliant with PCI-DSS Non-Root Container Security Standards
# ==============================================================================

FROM python:3.11-slim as builder

WORKDIR /build

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final minimal runtime image
FROM python:3.11-slim

LABEL maintainer="he99codes <priyanshu2164@gmail.com>" \
      service="payshield-payment-gateway" \
      domain="fintech-infrastructure"

WORKDIR /app

# Create non-root system user for PCI-DSS compliance
RUN groupadd -g 10001 payshield && \
    useradd -u 10001 -g payshield -m -s /bin/bash payshield

# Copy installed wheels/dependencies from builder
COPY --from=builder /root/.local /home/payshield/.local
COPY app.py .

ENV PATH=/home/payshield/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_VERSION=v2.4.0 \
    APP_ENV=production

RUN chown -R payshield:payshield /app
USER payshield

EXPOSE 5000

HEALTHCHECK --interval=15s --timeout=3s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/api/v1/health')" || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--access-logfile", "-", "app:app"]
