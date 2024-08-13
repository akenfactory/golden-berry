FROM documents-ms:0.0.0.0
ENV ENVIRONMENT pdn
ENV DEBUG false
ENV SECURITY_MANAGER_URL http://sec-svc.angel-ns.svc.cluster.local:5002/alive
COPY model ./
COPY src ./
RUN python download_nltk.py
ENTRYPOINT ["bash", "run.sh"]