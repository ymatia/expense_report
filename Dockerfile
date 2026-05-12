FROM python:3.12-slim-bookworm AS builder

COPY requirements.txt /
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --root-user-action=ignore -r /requirements.txt && rm /requirements.txt

FROM python:3.12-slim-bookworm

COPY --from=builder /usr/local/ /usr/local/
RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ADD /ex_app/li[b] /ex_app/lib
COPY --chmod=775 healthcheck.sh /
COPY --chmod=775 start.sh /

WORKDIR /ex_app/lib
ENTRYPOINT ["/start.sh", "python3", "main.py"]
# No Docker HEALTHCHECK: AppAPI only waits for this if the image defines one; a bad probe
# blocks deploy with "Container healthcheck failed". AppAPI then uses GET /heartbeat instead.
# Optional: docker run --health-cmd=/healthcheck.sh ... if you want engine-level checks.
