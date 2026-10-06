{
  description = "honiipy dev environment — uv provides the whole toolchain";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      # uv alone: it provisions python, and ruff, pytest, laconic, bandit and poe
      # all arrive as dev dependencies. `uv audit` needs uv >= 0.11.32.
      devShells = forAllSystems (pkgs: {
        default = pkgs.mkShell {
          packages = [ pkgs.uv ];
        };
      });
    };
}
