Gem::Specification.new do |s|
  s.name = 'honeybii'
  s.version = '3.0.0'
  s.date = '2026-02-21'
  s.executables << 'honeybii'
  s.add_runtime_dependency 'rmagick', '~> 6.0'
  s.required_ruby_version = '>= 3.0'
  s.files = ['lib/honeybii.rb', 'lib/honeybii/ascii_image.rb', 'lib/honeybii/shaded_ascii.rb']
  s.summary = 'An image-to-ascii converter'
  s.description = 'A command-line image-to-ascii conversion tool'
  s.authors = ['Jamey DeOrio']
  s.email = 'jamey@jameydeorio.com'
  s.homepage = 'http://honeybii.com'
  s.license = 'MIT'
end
