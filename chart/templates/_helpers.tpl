{{/* 공통 레이블 정의 */}}
{{- define "model-serving.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/* 네임스페이스 이름 정의 */}}
{{- define "model-serving.namespace" -}}
{{- .Values.global.namespace | default "model-serving" -}}
{{- end -}}