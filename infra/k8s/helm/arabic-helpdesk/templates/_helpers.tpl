{{/* Common labels */}}
{{- define "arabic-helpdesk.labels" -}}
app.kubernetes.io/name: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/* Image reference */}}
{{- define "arabic-helpdesk.image" -}}
{{- printf "%s/%s/%s:%s" .Values.image.registry .Values.image.repository .component (default .Chart.AppVersion .Values.image.tag) -}}
{{- end -}}
