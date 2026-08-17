# [Kevin Chuang — Senior Software Engineer](https://k-chuang.github.io)

Kevin Chuang's professional portfolio, built with Jekyll and the Minimal Mistakes theme and hosted on GitHub Pages.

Historical blog posts remain in the repository as an unpromoted archive so their existing URLs continue to work.

## Verify locally

Install the locked dependencies once:

```powershell
bundle install
```

Build the same Jekyll source used by GitHub Pages, then run the rendered-site test suite:

```powershell
$env:RUBYOPT = "-r./test/liquid_ruby_compat.rb"
bundle exec jekyll build --strict_front_matter
python test/site_test.py -v
```

Preview the verified output at `http://127.0.0.1:4000/`:

```powershell
python -m http.server 4000 --bind 127.0.0.1 --directory _site
```

The compatibility preload only restores APIs removed in Ruby 3.2 that are still used by the GitHub Pages 222 dependency set. It is a no-op on Ruby versions where those APIs exist.

## Deployment

The root GitHub Actions workflow builds with GitHub's Pages Jekyll action, runs the same rendered-site tests, packages the verified output, and only then starts the Pages deployment job. Configure the repository's Pages source as **GitHub Actions** before using this workflow to deploy.
