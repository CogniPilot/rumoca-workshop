{
  description = "Rumoca workshop maintainer tools and CI; attendees use uv or Codespaces";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      eachSystem = nixpkgs.lib.genAttrs systems;
      forSystem = system:
        let
          pkgs = import nixpkgs { inherit system; };
          tools = (with pkgs; [ uv python312 nodejs git gh ])
            ++ nixpkgs.lib.optionals pkgs.stdenv.hostPlatform.isLinux [ pkgs.devcontainer ];
          runtime = nixpkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc.lib pkgs.zlib ];
        in {
          devShell = pkgs.mkShell {
            packages = tools;
            JAX_PLATFORMS = "cpu";
            OMP_NUM_THREADS = "1";
            OPENBLAS_NUM_THREADS = "1";
            MKL_NUM_THREADS = "1";
            shellHook = ''
              export TMPDIR="$HOME/scratch/rumoca-workshop/tmp"
              export UV_CACHE_DIR="$HOME/scratch/rumoca-workshop/cache/uv"
              export UV_PROJECT_ENVIRONMENT="$HOME/scratch/rumoca-workshop/venv"
              mkdir -p "$TMPDIR" "$UV_CACHE_DIR"
              ${nixpkgs.lib.optionalString pkgs.stdenv.hostPlatform.isLinux ''export LD_LIBRARY_PATH="${runtime}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"''}
            '';
          };
          check = pkgs.writeShellApplication {
            name = "rumoca-workshop-check";
            runtimeInputs = tools;
            text = ''
              export TMPDIR="$HOME/scratch/rumoca-workshop/tmp"
              export UV_CACHE_DIR="$HOME/scratch/rumoca-workshop/cache/uv"
              export UV_PROJECT_ENVIRONMENT="$HOME/scratch/rumoca-workshop/venv"
              mkdir -p "$TMPDIR" "$UV_CACHE_DIR"
              ${nixpkgs.lib.optionalString pkgs.stdenv.hostPlatform.isLinux ''export LD_LIBRARY_PATH="${runtime}''${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"''}
              exec bash scripts/ci_checks.sh "$@"
            '';
          };
          container = pkgs.writeShellApplication {
            name = "rumoca-workshop-container-build";
            runtimeInputs = [ pkgs.docker-client ];
            text = ''
              # Run at the workshop repository root, against the tested Dockerfile.
              exec docker build -f .devcontainer/Dockerfile -t rumoca-workshop:local "$@" .
            '';
          };
        };
    in {
      devShells = eachSystem (system: {
        default = (forSystem system).devShell;
        ci = (forSystem system).devShell;
      });
      apps = eachSystem (system: {
        default = { type = "app"; program = "${(forSystem system).check}/bin/rumoca-workshop-check"; meta.description = "Run workshop CPU checks from the repository root"; };
        check = { type = "app"; program = "${(forSystem system).check}/bin/rumoca-workshop-check"; meta.description = "Run workshop CPU checks from the repository root"; };
        container-build = { type = "app"; program = "${(forSystem system).container}/bin/rumoca-workshop-container-build"; meta.description = "Build the tested Debian devcontainer with Docker"; };
      });
    };
}
