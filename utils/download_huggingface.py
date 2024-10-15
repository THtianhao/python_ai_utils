def download_from_huggingface(repo_id, file_path, models_dir):
    from huggingface_hub import hf_hub_download
    local_file_path = hf_hub_download(
        repo_id=repo_id,
        filename=file_path,
        local_dir=models_dir,
    )
    print(f"File downloaded to: {local_file_path}")

def download_from_huggingface_snapshot(repo_id, patterns, models_dir):
    from huggingface_hub import snapshot_download
    local_file_path = snapshot_download(
        repo_id=repo_id,
        allow_patterns=[patterns],
        local_dir=models_dir,
    )
    print(f"File downloaded to: {local_file_path}")
