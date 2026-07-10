import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django.db.models.functions import ExtractYear
from .forms import UploadFileForm
from .models import FileUploadLog, FactData

REQUIRED_COLUMNS = {"advertiser", "brand", "start", "end", "format", "platform", "impr"}


@login_required
def dashboard_view(request):
    """Handles file upload, data parsing, and dashboard rendering."""
    aggregated_data = (
        FactData.objects.annotate(year=ExtractYear("start_date"))
        .values("year")
        .annotate(total_impr=Sum("impressions"))
        .order_by("-year")
    )

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            file_name = uploaded_file.name

            try:
                if file_name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                elif file_name.endswith((".xls", ".xlsx")):
                    df = pd.read_excel(uploaded_file)
                else:
                    raise ValueError(
                        "Unsupported file format. Please use CSV or Excel."
                    )

                df.columns = [str(c).strip().lower() for c in df.columns]

                if not REQUIRED_COLUMNS.issubset(set(df.columns)):
                    raise ValueError(
                        f"Missing required columns. Expected: {REQUIRED_COLUMNS}"
                    )

                df = df.dropna(how="all")
                original_len = len(df)

                df["impr"] = pd.to_numeric(df["impr"], errors="coerce")
                df["start"] = pd.to_datetime(
                    df["start"], errors="coerce", dayfirst=True
                )
                df["end"] = pd.to_datetime(df["end"], errors="coerce", dayfirst=True)

                valid_df = df.dropna(subset=["impr", "start", "end"])
                valid_df = valid_df[valid_df["start"].dt.year > 2000]

                if original_len == 0 or len(valid_df) < (original_len * 0.8):
                    raise ValueError(
                        "Complete data mismatch: missing or invalid values in key columns."
                    )

                df = valid_df

                upload_log = FileUploadLog.objects.create(
                    user=request.user, file_name=file_name, status="SUCCESS"
                )

                fact_data_objects = [
                    FactData(
                        upload_log=upload_log,
                        advertiser=str(row["advertiser"])[:255],
                        brand=str(row["brand"])[:255],
                        start_date=row["start"],
                        end_date=row["end"],
                        ad_format=str(row["format"])[:100],
                        platform=str(row["platform"])[:100],
                        impressions=int(row["impr"]),
                    )
                    for _, row in df.iterrows()
                ]

                FactData.objects.bulk_create(fact_data_objects, batch_size=1000)
                messages.success(request, f"File {file_name} successfully processed.")

            except Exception as e:
                FileUploadLog.objects.create(
                    user=request.user,
                    file_name=file_name,
                    status="FAILED",
                    error_type=str(e),
                )
                messages.error(request, f"Error processing file: {str(e)}")

            return redirect("dashboard")
    else:
        form = UploadFileForm()

    return render(
        request,
        "analytics/dashboard.html",
        {"form": form, "aggregated_data": aggregated_data},
    )
