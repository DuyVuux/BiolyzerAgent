package stage10

import (
	"go/ast"
	"go/parser"
	"go/token"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestStage10DoesNotImportDistributedInfrastructure(t *testing.T) {
	root := repoRoot(t)
	targets := []string{
		filepath.Join(root, "internal", "persistence"),
		filepath.Join(root, "internal", "platform", "persistence"),
		filepath.Join(root, "internal", "platform", "runtime", "persistentlocal"),
	}
	forbidden := []string{"redis", "dbos", "kafka", "celery", "pgx", "postgres", "nats", "rabbitmq", "temporal"}
	for _, dir := range targets {
		err := filepath.Walk(dir, func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if info.IsDir() || !strings.HasSuffix(path, ".go") || strings.HasSuffix(path, "_test.go") {
				return nil
			}
			f, err := parser.ParseFile(token.NewFileSet(), path, nil, parser.ImportsOnly)
			if err != nil {
				return err
			}
			for _, imp := range f.Imports {
				name := strings.Trim(imp.Path.Value, `"`)
				for _, bad := range forbidden {
					if strings.Contains(strings.ToLower(name), bad) {
						t.Errorf("%s imports deferred infrastructure %q", path, name)
					}
				}
			}
			_ = ast.File{}
			return nil
		})
		if err != nil {
			t.Fatal(err)
		}
	}
}

func repoRoot(t *testing.T) string {
	t.Helper()
	dir, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	for i := 0; i < 6; i++ {
		if _, err := os.Stat(filepath.Join(dir, "go.mod")); err == nil {
			return dir
		}
		dir = filepath.Dir(dir)
	}
	t.Fatal("repo root not found")
	return ""
}
